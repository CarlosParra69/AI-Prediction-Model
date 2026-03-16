"""
Scorer para preguntas de tipo ORDERING (reordenar elementos).

Evaluación:
- Puntuación exacta: todos los elementos en posición correcta → 1.0
- Puntuación parcial: proporción de elementos en posición correcta
- Bonus por pares adyacentes en orden correcto
- Compatible con exámenes multilingües (fr/en)
"""

from __future__ import annotations

from typing import List, Tuple

from ..schemas import Language


def score_ordering(
    answer_list: List[str],
    correct_order: List[str],
    language: Language = Language.fr,
) -> Tuple[float, float, str]:
    """
    Evalúa la respuesta a una pregunta de ordenar elementos.

    Lógica de puntuación (normalizada a 0-1):
    - Posiciones correctas    → 60% del score
    - Pares adyacentes OK     → 40% del score (premia orden relativo)

    Args:
        answer_list:   Lista de elementos en el orden elegido por el candidato.
        correct_order: Lista de elementos en el orden correcto.
        language:      Idioma de la pregunta.

    Returns:
        Tupla (score, confidence, explanation).
    """
    if not correct_order:
        return 0.5, 0.3, _msg("no_correct_defined", language)

    if not answer_list:
        return 0.0, 1.0, _msg("empty", language)

    n = len(correct_order)

    # Normalizar: minúsculas + strip
    answer_norm = [a.strip().lower() for a in answer_list]
    correct_norm = [c.strip().lower() for c in correct_order]

    # ── Componente 1: posiciones correctas ───────────────────────────────────
    position_hits = sum(
        1 for i, item in enumerate(answer_norm)
        if i < n and item == correct_norm[i]
    )
    position_score = position_hits / n if n > 0 else 0.0

    # ── Componente 2: pares adyacentes en orden correcto ─────────────────────
    if n > 1:
        correct_pairs = set(zip(correct_norm[:-1], correct_norm[1:]))
        answer_pairs = set(zip(answer_norm[:-1], answer_norm[1:]))
        pair_hits = len(correct_pairs & answer_pairs)
        pair_score = pair_hits / len(correct_pairs) if correct_pairs else 0.0
    else:
        pair_score = 1.0 if position_score == 1.0 else 0.0

    # Score final ponderado
    score = min(1.0, position_score * 0.6 + pair_score * 0.4)
    confidence = 0.97

    explanation = _build_explanation(
        position_hits=position_hits,
        n=n,
        pair_score=pair_score,
        score=score,
        language=language,
    )

    return score, confidence, explanation


def _build_explanation(
    position_hits: int,
    n: int,
    pair_score: float,
    score: float,
    language: Language,
) -> str:
    lang = language.value if hasattr(language, "value") else str(language)

    if lang == "en":
        parts = [f"{position_hits}/{n} elements in correct position."]
        if pair_score >= 0.8:
            parts.append("Good relative ordering.")
        elif pair_score >= 0.5:
            parts.append("Partial relative ordering.")
        else:
            parts.append("Mostly incorrect ordering.")
        if score == 1.0:
            parts.append("Perfect answer.")
    else:
        parts = [f"{position_hits}/{n} elementos en posición correcta."]
        if pair_score >= 0.8:
            parts.append("Buen orden relativo.")
        elif pair_score >= 0.5:
            parts.append("Orden relativo parcial.")
        else:
            parts.append("Orden mayoritariamente incorrecto.")
        if score == 1.0:
            parts.append("Respuesta perfecta.")

    return " ".join(parts)


def _msg(key: str, language: Language) -> str:
    msgs: dict[str, dict[str, str]] = {
        "no_correct_defined": {
            "fr": "Aucun ordre correct défini pour cette question.",
            "en": "No correct order defined for this question.",
        },
        "empty": {
            "fr": "Réponse vide — aucun élément soumis.",
            "en": "Empty response — no elements submitted.",
        },
    }
    lang_key = language.value if hasattr(language, "value") else str(language)
    return msgs.get(key, {}).get(lang_key, msgs.get(key, {}).get("fr", key))
