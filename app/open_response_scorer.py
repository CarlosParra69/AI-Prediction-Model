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
from .french_scorer import (
    FRENCH_CONNECTORS_BY_LEVEL,
    FRENCH_POLITENESS_MARKERS,
    score_morphosyntax_fr,
    score_coherence_fr,
    score_sociolinguistic_fr,
    score_lexicon_fr,
)
from .english_scorer import (
    ENGLISH_CONNECTORS_BY_LEVEL,
    ENGLISH_POLITENESS_MARKERS,
    score_morphosyntax_en,
    score_coherence_en,
    score_sociolinguistic_en,
    score_lexicon_en,
)


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
            language=language,
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
        """Evalúa coherencia y cohesión (delega a módulo de idioma específico)."""
        if language == Language.en:
            return score_coherence_en(response_text, word_count, text_lower)
        else:
            return score_coherence_fr(response_text, word_count, text_lower)

    def _score_sociolinguistic(self, text_lower: str, language: Language) -> float:
        """Evalúa adecuación sociolingüística (delega a módulo de idioma específico)."""
        if language == Language.en:
            return score_sociolinguistic_en(text_lower)
        else:
            return score_sociolinguistic_fr(text_lower)

    def _score_lexicon(self, text_lower: str, word_count: int, language: Language) -> float:
        """Evalúa variedad de vocabulario (delega a módulo de idioma específico)."""
        if language == Language.en:
            return score_lexicon_en(text_lower, word_count)
        else:
            return score_lexicon_fr(text_lower, word_count)

    def _score_morphosyntax(self, response_text: str, text_lower: str, language: Language) -> float:
        """Evalúa morfosintaxis (delega a módulo de idioma específico)."""
        if language == Language.en:
            return score_morphosyntax_en(response_text, text_lower)
        else:
            return score_morphosyntax_fr(response_text, text_lower)

    def _compute_confidence(
        self,
        word_count: int,
        rubric: OpenQuestionRubric,
        breakdown: RubricBreakdown,
    ) -> float:
        """Calcula la confianza penalizando por errores detectados."""
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
        
        # Penalize if morphosyntax or lexicon is weak (error indicators)
        error_penalty = 0.0
        if breakdown.morphosyntax < 0.65:
            error_penalty += 0.15
        if breakdown.lexicon < 0.55:
            error_penalty += 0.10
        if breakdown.sociolinguistic < 0.55:
            error_penalty += 0.08

        confidence = (length_factor * 0.6 + consistency_factor * 0.4) - error_penalty
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
