"""
Scorer para preguntas de tipo FILL_BLANK (rellenar huecos).

Evaluación:
- Acepta múltiples respuestas válidas
- Tolerancia a variaciones de acento (normalización Unicode)
- Tolerancia a espacios extra
- Compatible con exámenes multilingües (fr/en)
"""

from __future__ import annotations

import unicodedata
from typing import List, Optional, Tuple

from ..schemas import Language


def _normalize(text: str) -> str:
    """Elimina acentos y convierte a minúsculas para comparación flexible."""
    nfkd = unicodedata.normalize("NFKD", text.lower().strip())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def score_fill_blank(
    answer_text: str,
    accepted_answers: List[str],
    language: Language = Language.fr,
) -> Tuple[float, float, str]:
    """
    Evalúa la respuesta a una pregunta de rellenar hueco.

    Lógica de puntuación:
    - Coincidencia exacta (normalizada)  → 1.0
    - Coincidencia sin acento            → 0.85 (variación menor)
    - Sin coincidencia                   → 0.0

    Args:
        answer_text:      Texto de respuesta del candidato.
        accepted_answers: Lista de respuestas consideradas correctas.
        language:         Idioma de la pregunta (para mensajes de feedback).

    Returns:
        Tupla (score, confidence, explanation).
    """
    if not accepted_answers:
        return 0.5, 0.3, _msg("no_correct_defined", language)

    if not answer_text or not answer_text.strip():
        return 0.0, 1.0, _msg("empty", language)

    candidate = answer_text.strip().lower()
    candidate_norm = _normalize(candidate)

    # Paso 1: coincidencia exacta (insensible a mayúsculas)
    for accepted in accepted_answers:
        if candidate == accepted.strip().lower():
            return 1.0, 0.98, _msg("correct", language)

    # Paso 2: coincidencia sin acento
    for accepted in accepted_answers:
        if candidate_norm == _normalize(accepted):
            note = _msg("correct_accent", language)
            return 0.85, 0.92, note

    return 0.0, 0.97, _msg("incorrect", language, accepted_answers)


def score_fill_blank_multi(
    answer_texts: List[str],
    accepted_answers_per_blank: List[List[str]],
    language: Language = Language.fr,
) -> Tuple[float, float, str]:
    """
    Evalúa una pregunta con múltiples huecos.

    Aplica ``score_fill_blank`` a cada hueco y promedia los scores.

    Args:
        answer_texts:              Lista de respuestas del candidato (una por hueco).
        accepted_answers_per_blank: Lista de listas de respuestas aceptadas por hueco.
        language:                  Idioma de la pregunta.

    Returns:
        Tupla (score_promedio, confidence, explanation).
    """
    if not accepted_answers_per_blank:
        return 0.5, 0.3, _msg("no_correct_defined", language)

    n_blanks = len(accepted_answers_per_blank)
    scores: List[float] = []
    confidences: List[float] = []

    for i, accepted in enumerate(accepted_answers_per_blank):
        ans = answer_texts[i] if i < len(answer_texts) else ""
        s, c, _ = score_fill_blank(ans, accepted, language)
        scores.append(s)
        confidences.append(c)

    avg_score = sum(scores) / n_blanks
    avg_conf = sum(confidences) / n_blanks
    correct_count = sum(1 for s in scores if s >= 0.85)

    if language == Language.en:
        explanation = f"{correct_count}/{n_blanks} blanks correct."
    else:
        explanation = f"{correct_count}/{n_blanks} huecos correctos."

    return avg_score, avg_conf, explanation


# ── Mensajes de feedback ─────────────────────────────────────────────────────

def _msg(key: str, language: Language, accepted: Optional[List[str]] = None) -> str:
    msgs: dict[str, dict[str, str]] = {
        "correct": {
            "fr": "Réponse correcte.",
            "en": "Correct answer.",
        },
        "correct_accent": {
            "fr": "Réponse correcte (variation d'accent acceptée).",
            "en": "Correct answer (minor accent variation accepted).",
        },
        "incorrect": {
            "fr": "Réponse incorrecte.",
            "en": "Incorrect answer.",
        },
        "empty": {
            "fr": "Réponse vide.",
            "en": "Empty answer.",
        },
        "no_correct_defined": {
            "fr": "Aucune réponse correcte définie pour cette question.",
            "en": "No correct answer defined for this question.",
        },
    }
    lang_key = language.value if hasattr(language, "value") else str(language)
    text = msgs.get(key, {}).get(lang_key, msgs.get(key, {}).get("fr", key))
    return text
