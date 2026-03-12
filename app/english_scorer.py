"""Módulo específico para evaluación de respuestas en inglés."""

from __future__ import annotations

import re

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


def score_morphosyntax_en(response_text: str, text_lower: str) -> float:
    """Detección de errores de morfosintaxis en inglés."""
    errors = 0
    
    # Common conjugation errors
    conj_patterns = [
        r"\bi\s+am[s]?",
        r"\bhe\s+are\b",
        r"\bshe\s+are\b",
        r"\bthey\s+is\b",
        r"\byou\s+is\b",
    ]
    errors += sum(1 for p in conj_patterns if re.search(p, text_lower))
    
    # Article errors
    article_patterns = [
        r"\ba\s+[aeiou]",
        r"\ban\s+[^aeiou]",
    ]
    errors += sum(1 for p in article_patterns if re.search(p, text_lower))
    
    base = 0.85
    penalty_per_error = 0.08
    return max(0.3, base - (errors * penalty_per_error))


def score_coherence_en(
    response_text: str,
    word_count: int,
    text_lower: str,
) -> float:
    """Evalúa coherencia específica para inglés."""
    connector_count = sum(
        1 for connectors in ENGLISH_CONNECTORS_BY_LEVEL.values()
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


def score_sociolinguistic_en(text_lower: str) -> float:
    """Evalúa adecuación sociolingüística en inglés."""
    original_words = text_lower.split()
    
    # Check for excessive caps
    all_caps_count = sum(1 for w in original_words if w.isupper() and len(w) > 1)
    if all_caps_count > len(original_words) * 0.3:
        return 0.3

    if len(original_words) < 5:
        return 0.4
    
    score = 0.65
    
    # Check for politeness markers
    has_politeness = any(marker in text_lower for marker in ENGLISH_POLITENESS_MARKERS)
    if has_politeness:
        score = 0.80
    
    return min(1.0, score)


def score_lexicon_en(text_lower: str, word_count: int) -> float:
    """Evalúa variedad de vocabulario en inglés."""
    if word_count < 5:
        return 0.2

    words = text_lower.split()
    
    common_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "and", "or", "but", "not", "no", "yes", "i", "you", "he", "she", "it",
        "we", "they", "what", "which", "who", "where", "when", "why", "how",
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
