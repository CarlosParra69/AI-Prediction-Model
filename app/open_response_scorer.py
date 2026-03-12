"""
Módulo para evaluar respuestas abiertas usando criterios DELF (CEFR).

Implementa scoring híbrido multiidioma (francés e inglés):
- Basado en reglas + detección de palabras clave
- Análisis de conectores y estructura
- Tolerancia a errores menores (ESL principles)
- Si la confianza es baja, marca para revisión humana.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from .schemas import Language, OpenQuestionRubric, RubricBreakdown


# ============================================================================
# FRENCH CONNECTORS AND LINGUISTIC FEATURES
# ============================================================================
FRENCH_CONNECTORS_BY_LEVEL = {
    "A1": {"et", "mais", "parce que", "alors"},
    "A1+": {"et", "mais", "parce que", "alors", "aussi", "car"},
    "A2": {"et", "mais", "parce que", "alors", "aussi", "car", "cependant", "ensuite", "d'abord"},
    "A2+": {"et", "mais", "parce que", "alors", "aussi", "car", "cependant", "ensuite", "d'abord", "puis", "auparavant"},
    "B1": {"en effet", "cependant", "donc", "toutefois", "de plus", "par contre", "d'ailleurs", "finalement"},
    "B1+": {"en effet", "cependant", "donc", "toutefois", "de plus", "par contre", "d'ailleurs", "finalement", "bien que", "pourvu que"},
    "B2": {"en effet", "cependant", "donc", "toutefois", "de plus", "par contre", "d'ailleurs", "finalement", "bien que", "pourvu que", "néanmoins", "ainsi", "notamment"},
}

FRENCH_POLITENESS_MARKERS = {
    "s'il vous plaît", "s'il te plaît", "merci", "merci beaucoup",
    "cordialement", "sincères salutations", "bien à vous"
}


# ============================================================================
# ENGLISH CONNECTORS AND LINGUISTIC FEATURES
# ============================================================================
ENGLISH_CONNECTORS_BY_LEVEL = {
    "A1": {"and", "but", "because", "so", "then"},
    "A1+": {"and", "but", "because", "so", "then", "also", "after", "before"},
    "A2": {"and", "but", "because", "so", "then", "also", "after", "before", "however", "for example", "first"},
    "A2+": {"and", "but", "because", "so", "then", "also", "after", "before", "however", "for example", "first", "finally", "next", "in addition"},
    "B1": {"however", "therefore", "moreover", "for instance", "in conclusion", "in addition", "on the other hand", "nevertheless"},
    "B1+": {"however", "therefore", "moreover", "for instance", "in conclusion", "in addition", "on the other hand", "nevertheless", "although", "despite", "provided that"},
    "B2": {"nonetheless", "furthermore", "consequently", "in particular", "as a matter of fact", "in summary", "to illustrate", "nevertheless", "although", "despite", "provided that", "whereas"},
}

ENGLISH_POLITENESS_MARKERS = {
    "please", "thank you", "thanks", "kind regards", "best regards",
    "sincerely", "yours truly", "with appreciation"
}


# ============================================================================
# LANGUAGE DETECTION
# ============================================================================
def detect_language(text: str) -> Language:
    """
    Detecta el idioma del texto basado en palabras y patrones.
    
    Heurística simple:
    - Busca palabras características francesas vs inglesas
    - Si es ambiguo, asume francés (por defecto)
    
    Args:
        text: Texto a analizar
        
    Returns:
        Language.en o Language.fr
    """
    if not text or not text.strip():
        return Language.fr  # Default a francés
    
    text_lower = text.lower()
    
    # Palabras muy características del francés
    french_markers = {
        "je", "tu", "il", "elle", "nous", "vous", "ils", "elles",  # pronouns
        "le", "la", "les", "un", "une", "des",  # articles
        "pas", "ne", "qu'à", "d'où", "partout",  # negatives/questions
        "café", "boulangerie", "château", "musée", "théâtre",  # typical words
        "aujourd'hui", "demain", "hier", "semaine", "mois",  # common words
    }
    
    # Palabras muy características del inglés
    english_markers = {
        "the", "is", "are", "was", "were", "be", "been", "being",  # articles & verbs
        "a", "an", "this", "that", "these", "those",  # determiners
        "and", "or", "but", "if", "because",  # conjunctions
        "will", "would", "should", "could", "may", "might", "must", "can",  # modals
        "very", "really", "quite", "rather", "fairly",  # adverbs
    }
    
    words = set(text_lower.split())
    
    french_score = len(words & french_markers)
    english_score = len(words & english_markers)
    
    # Si el score de inglés es significativamente mayor
    if english_score > french_score + 2:
        return Language.en
    
    return Language.fr  # Default a francés si es ambiguo


@dataclass
class OpenResponseScore:
    """Resultado de evaluación de respuesta abierta."""

    score: float  # 0-1
    rubric_breakdown: RubricBreakdown
    confidence: float  # 0-1
    needs_human_review: bool
    explanation: str
    language_detected: Language  # Idioma detectado/usado


class OpenResponseScorer:
    """
    Evaluador de respuestas abiertas con criterios DELF/CEFR multiidioma.
    
    Soporta evaluación en francés e inglés usando los mismos criterios DELF,
    pero con reglas lingüísticas específicas para cada idioma:
    - Conectores propios de cada nivel
    - Marcadores de cortesía específicos
    - Tolerancia a errores según ESL principles
    
    Marca para revisión humana si confianza < threshold.
    """

    def __init__(self, confidence_threshold: float = 0.6):
        """
        Args:
            confidence_threshold: Umbral para marcar revisión humana.
        """
        self.confidence_threshold = confidence_threshold

    def score(
        self,
        response_text: str,
        rubric: OpenQuestionRubric,
        language: Optional[Language] = None,
        expected_keywords: Optional[list[str]] = None,
    ) -> OpenResponseScore:
        """
        Evalúa una respuesta abierta contra una rúbrica DELF.

        Args:
            response_text: Texto de la respuesta del candidato.
            rubric: Rúbrica DELF con criterios y nivel esperado.
            language: Idioma de la respuesta (fr|en). Si es None, detecta automáticamente.
            expected_keywords: Lista de palabras clave esperadas (opcional).

        Returns:
            OpenResponseScore con desglose por criterio DELF.
        """
        # Detectar idioma si no se especifica
        if language is None:
            language = detect_language(response_text)
        
        # Validación: respuesta vacía o muy corta
        if not response_text or not response_text.strip():
            return OpenResponseScore(
                score=0.0,
                rubric_breakdown=RubricBreakdown(
                    task_realisation=0.0,
                    coherence=0.0,
                    sociolinguistic=0.0,
                    lexicon=0.0,
                    morphosyntax=0.0,
                ),
                confidence=1.0,
                needs_human_review=False,
                explanation="Empty response." if language == Language.en else "Respuesta vacía.",
                language_detected=language,
            )

        # Normalizar texto
        text_lower = response_text.lower().strip()
        words = text_lower.split()
        word_count = len(words)

        # Calcula breakdown por criterio
        breakdown = self._compute_rubric_breakdown(
            response_text=response_text,
            word_count=word_count,
            rubric=rubric,
            language=language,
            expected_keywords=expected_keywords or [],
        )

        # Score ponderado
        score = breakdown.weighted_score(rubric.criteria_weights)

        # Calcula confianza
        confidence = self._compute_confidence(
            word_count=word_count,
            rubric=rubric,
            breakdown=breakdown,
        )

        # Determina revisión humana
        needs_review = confidence < self.confidence_threshold

        # Explicación
        explanation = self._build_explanation(
            word_count=word_count,
            rubric=rubric,
            breakdown=breakdown,
            confidence=confidence,
            language=language,
        )

        return OpenResponseScore(
            score=float(score),
            rubric_breakdown=breakdown,
            confidence=float(confidence),
            needs_human_review=needs_review,
            explanation=explanation,
            language_detected=language,
        )

    def _compute_rubric_breakdown(
        self,
        response_text: str,
        word_count: int,
        rubric: OpenQuestionRubric,
        language: Language,
        expected_keywords: list[str],
    ) -> RubricBreakdown:
        """Calcula el breakdown por criterio DELF."""
        text_lower = response_text.lower()

        task_score = self._score_task_realisation(
            word_count=word_count,
            text_lower=text_lower,
            rubric=rubric,
            expected_keywords=expected_keywords,
        )

        coherence_score = self._score_coherence(
            response_text=response_text,
            word_count=word_count,
            text_lower=text_lower,
            language=language,
        )

        socio_score = self._score_sociolinguistic(
            text_lower=text_lower,
            language=language,
        )

        lexicon_score = self._score_lexicon(
            text_lower=text_lower,
            word_count=word_count,
        )

        morphosyntax_score = self._score_morphosyntax(
            response_text=response_text,
            text_lower=text_lower,
            language=language,
        )

        return RubricBreakdown(
            task_realisation=float(task_score),
            coherence=float(coherence_score),
            sociolinguistic=float(socio_score),
            lexicon=float(lexicon_score),
            morphosyntax=float(morphosyntax_score),
        )

    def _score_task_realisation(
        self,
        word_count: int,
        text_lower: str,
        rubric: OpenQuestionRubric,
        expected_keywords: list[str],
    ) -> float:
        """Evalúa si se realizó la tarea (longitud mínima + keywords)."""
        min_words = rubric.expected_min_words
        target_words = max(min_words * 2, 50)

        if word_count < min_words:
            length_score = max(0.1, word_count / min_words * 0.4)
        elif word_count <= target_words:
            length_score = 0.4 + (word_count - min_words) / (target_words - min_words) * 0.35
        else:
            length_score = min(0.8, 0.75 + (word_count - target_words) / 100 * 0.05)

        keywords_score = 0.2
        if expected_keywords:
            found = sum(1 for kw in expected_keywords if kw.lower() in text_lower)
            keywords_score = 0.2 + (found / len(expected_keywords) * 0.2)

        return min(1.0, length_score + keywords_score)

    def _score_coherence(
        self,
        response_text: str,
        word_count: int,
        text_lower: str,
        language: Language,
    ) -> float:
        """Evalúa coherencia y cohesión (estructura, conectores, puntuación)."""
        connectors_pool = (
            ENGLISH_CONNECTORS_BY_LEVEL if language == Language.en
            else FRENCH_CONNECTORS_BY_LEVEL
        )
        
        connector_count = sum(
            1 for connectors in connectors_pool.values()
            for conn in connectors
            if conn in text_lower
        )
        
        connector_score = min(0.5, connector_count * 0.1) if word_count > 10 else 0.2

        punctuation_count = text_lower.count(".") + text_lower.count(",") + text_lower.count("?")
        punctuation_score = min(0.3, punctuation_count * 0.05) if word_count > 5 else 0.1

        sentences = response_text.replace("?", ".").split(".")
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) > 1:
            avg_sent_len = word_count / len(sentences)
            sent_score = 0.2
            if 3 <= avg_sent_len <= 15:
                sent_score = 0.35
            elif avg_sent_len > 5:
                sent_score = 0.3
        else:
            sent_score = 0.1

        return min(1.0, connector_score + punctuation_score + sent_score)

    def _score_sociolinguistic(self, text_lower: str, language: Language) -> float:
        """Evalúa adecuación sociolingüística (registro, tono)."""
        original_words = text_lower.split()
        all_caps_count = sum(1 for w in original_words if w.isupper() and len(w) > 1)
        
        if all_caps_count > len(original_words) * 0.3:
            return 0.3

        if len(original_words) < 5:
            return 0.4
        
        politeness_markers = (
            ENGLISH_POLITENESS_MARKERS if language == Language.en
            else FRENCH_POLITENESS_MARKERS
        )
        
        has_politeness = any(marker in text_lower for marker in politeness_markers)
        if has_politeness:
            return 0.75
        
        return 0.65

    def _score_lexicon(self, text_lower: str, word_count: int) -> float:
        """Evalúa variedad de vocabulario."""
        if word_count < 5:
            return 0.2

        words = text_lower.split()
        
        common_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "and", "or", "but", "not", "no", "yes", "i", "you", "he", "she", "it",
            "we", "they", "what", "which", "who", "where", "when", "why", "how",
            "le", "la", "les", "un", "une", "des", "est", "sont", "être", "eu",
            "et", "ou", "mais", "ne", "non", "pas", "je", "tu", "il", "elle",
            "nous", "vous", "ils", "elles", "quoi", "quel", "qui", "où", "quand", "comment",
        }
        
        content_words = [w for w in words if w not in common_words and len(w) > 2]
        unique_words = len(set(content_words))
        content_count = len(content_words)
        
        diversity = unique_words / content_count if content_count > 0 else 0
        
        if diversity > 0.7:
            return 0.8
        elif diversity > 0.5:
            return 0.6
        elif diversity > 0.3:
            return 0.4
        else:
            return 0.2

    def _score_morphosyntax(self, response_text: str, text_lower: str, language: Language) -> float:
        """Evalúa morfosintaxis con tolerancia ESL."""
        if language == Language.en:
            verb_patterns = [r"\w+ing\b", r"\w+ed\b", r"\w+s\b"]
        else:
            verb_patterns = [r"\w+ais\b", r"\w+ait\b", r"\w+ent\b", r"\w+ions\b"]
        
        verb_score = 0.3
        for pattern in verb_patterns:
            if re.search(pattern, text_lower):
                verb_score = 0.5
                break

        allowed_accents = "éèêëàâäôöûüçñ"
        illegal_chars = sum(
            1 for c in response_text 
            if ord(c) > 127 and c not in allowed_accents
        )
        char_score = 1.0 if illegal_chars == 0 else max(0.1, 1.0 - illegal_chars * 0.1)

        punctuation_score = 0.5
        if response_text.count(".") > 0 or response_text.count("!") > 0 or response_text.count("?") > 0:
            punctuation_score = 0.7

        return min(1.0, (verb_score + char_score + punctuation_score) / 3 * 1.2)

    def _compute_confidence(
        self,
        word_count: int,
        rubric: OpenQuestionRubric,
        breakdown: RubricBreakdown,
    ) -> float:
        """Calcula la confianza de la evaluación."""
        min_words = rubric.expected_min_words

        if word_count < min_words:
            length_factor = 0.3 + (word_count / min_words) * 0.3
        elif word_count < min_words * 2:
            length_factor = 0.7
        else:
            length_factor = 0.85

        scores = [
            breakdown.task_realisation,
            breakdown.coherence,
            breakdown.sociolinguistic,
            breakdown.lexicon,
            breakdown.morphosyntax,
        ]
        avg_score = sum(scores) / len(scores)
        variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)
        std_dev = variance ** 0.5

        consistency_factor = max(0.2, 1.0 - std_dev)

        confidence = length_factor * 0.6 + consistency_factor * 0.4
        return min(1.0, max(0.1, confidence))

    def _build_explanation(
        self,
        word_count: int,
        rubric: OpenQuestionRubric,
        breakdown: RubricBreakdown,
        confidence: float,
        language: Language,
    ) -> str:
        """Construye una explicación legible de la evaluación."""
        parts = []
        
        is_english = language == Language.en

        if word_count < rubric.expected_min_words:
            if is_english:
                parts.append(f"Insufficient length ({word_count} words, minimum {rubric.expected_min_words}).")
            else:
                parts.append(f"Longitud insuficiente ({word_count} palabras, mínimo {rubric.expected_min_words}).")
        else:
            if is_english:
                parts.append(f"Adequate length ({word_count} words).")
            else:
                parts.append(f"Longitud adecuada ({word_count} palabras).")

        if is_english:
            criteria_names = {
                "task_realisation": "Task Realisation",
                "coherence": "Coherence and Cohesion",
                "sociolinguistic": "Sociolinguistic Adequacy",
                "lexicon": "Lexical Range",
                "morphosyntax": "Morphosyntax",
            }
        else:
            criteria_names = {
                "task_realisation": "Réalisation de la tâche",
                "coherence": "Cohérence/Cohésion",
                "sociolinguistic": "Adéquation sociolinguistique",
                "lexicon": "Lexique",
                "morphosyntax": "Morphosyntaxe",
            }
        
        weakest = min(
            [("task_realisation", breakdown.task_realisation),
             ("coherence", breakdown.coherence),
             ("sociolinguistic", breakdown.sociolinguistic),
             ("lexicon", breakdown.lexicon),
             ("morphosyntax", breakdown.morphosyntax)],
            key=lambda x: x[1],
        )
        
        if weakest[1] < 0.5:
            if is_english:
                parts.append(f"Weakness: {criteria_names[weakest[0]]} (score: {weakest[1]:.2f}).")
            else:
                parts.append(f"Punto débil: {criteria_names[weakest[0]]} (score: {weakest[1]:.2f}).")

        if confidence < 0.6:
            if is_english:
                parts.append(f"Low confidence ({confidence:.2f}). Manual review required.")
            else:
                parts.append(f"Confianza baja ({confidence:.2f}). Requiere revisión humana.")

        return " ".join(parts) if parts else ("No comments." if is_english else "Sin comentarios.")

    def reconcile_scores(
        self,
        auto_score: float,
        human_score: float,
        human_weight: float = 0.8,
    ) -> float:
        """Reconcilia score automático con score humano."""
        return human_weight * human_score + (1 - human_weight) * auto_score
