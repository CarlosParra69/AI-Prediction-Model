"""Módulo específico para evaluación de respuestas en francés."""

from __future__ import annotations

import re
from typing import List

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

FRENCH_GRAMMAR_ERRORS = {
    # Contraction errors
    r"\bque\s+je\b": "que j'",  # que je + vowel = que j'
    r"\bque\s+il\b": "que l'",
    r"\bque\s+elle\b": "que l'",
    r"\bde\s+un\b": "d'un",
    r"\bde\s+une\b": "d'une",
    # Common conjugation errors for present indicative
    r"\bje\s+aimes\b": "je aime",
    r"\bj'aimes\b": "j'aime",
    r"\btu\s+aime\b": "tu aimes",
    r"\bells\s+aimez\b": "elles aiment",
    r"\bnous\s+aimes\b": "nous aimons",
    # Verb être errors  
    r"\bj'étaient\b": "j'étais or j'était",
    r"\bil\s+étaient\b": "elle était or il était",
    # Common spelling/accent errors
    r"dificile": "difficile",
    r"casserolle": "casserole",
    r"legume": "légume",
    r"cuisne": "cuisine",
    r"parentés": "parentes",
    r"fieres": "fières",
    r"famile": "famille",
    r"alé": "allé",
    r"beacoup": "beaucoup",
}

FRENCH_INFORMAL_MARKERS = {
    "ca,c est": "ça, c'est",
    " ca ": " ça ",
    " ya ": " il y a ",
    "ptetre": "peut-être",
    "tjrs": "toujours",
    "qd": "quand",
    "pq": "pourquoi",
    "sympa": "sympathique",
    "enorme": "énorme",
    "super": "très",
}

FRENCH_FORMAL_SIGNALS = [
    "je considère",
    "en ce qui concerne",
    "d'ailleurs",
    "de plus",
    "en effet",
    "toutefois",
    "néanmoins",
]

FRENCH_SPELLING_ERRORS = {
    "dificile": ("difficile", 0.05),
    "casserolle": ("casserole", 0.05),
    "legume": ("légume", 0.05),
    "beacoup": ("beaucoup", 0.06),
    "cuisne": ("cuisine", 0.05),
    "parentés": ("parentes", 0.06),
    "fieres": ("fières", 0.04),
    "famile": ("famille", 0.06),
    "alé": ("allé", 0.05),
    "environement": ("environnement", 0.04),
    "quietud": ("quiétude", 0.05),
    "memorable": ("mémorable", 0.04),
    "nouriture": ("nourriture", 0.06),
    "experience": ("expérience", 0.03),
    "encor": ("encore", 0.05),
    "vrement": ("vraiment", 0.05),
}


def score_morphosyntax_fr(response_text: str, text_lower: str) -> float:
    """Detecta errores de conjugación, contracción y ortografía en francés."""
    errors = []
    
    # Contraction errors
    contractions = [
        (r"\bque\s+je\b", "que j'"),
        (r"\bde\s+un\b", "d'un"),
        (r"\bde\s+une\b", "d'une"),
        (r"\bde\s+il\b", "de lui / du"),
    ]
    for pattern, fix in contractions:
        if re.search(pattern, text_lower):
            errors.append(("contraction", 0.08))
    
    # Conjugation errors (subject-verb agreement)
    conj_errors = [
        (r"\bj[e']?\s+aimes\b", "je aime"),
        (r"\btu\s+aime\s", "tu aimes"),
        (r"\belle\s+aimons\b", "elle aime"),
        (r"\bnous\s+aimes\b", "nous aimons"),
        (r"\billÉ?s\s+sommes\b", "ils sont"),
        (r"\bell[e]?s\s+suis\b", "elles sont"),
        (r"\bj[e']?.*étaient\b", "j'étais"),
    ]
    for pattern, suggestion in conj_errors:
        if re.search(pattern, text_lower):
            errors.append(("conjugation", 0.12))
    
    # Spelling/Accent errors
    spelling_errors = [
        r"dificile", r"casserolle", r"legume", r"cuisne", r"parentés",
        r"fieres", r"famile", r"alé", r"beacoup", r"riconctr",
        r"enrichissante", r"nouriture", r"nourriture", r"oublier",
        r"differente|différente", r"environement|environnement",
        r"quietud", r"lumieres", r"memorable", r"enrichissante",
        r"vrement", r"experience",
    ]
    
    for error_pattern in spelling_errors:
        if re.search(error_pattern, text_lower):
            errors.append(("spelling", 0.06))
    
    # Gender/Number agreement errors  
    gender_errors = [
        (r"\bun\s+place\b", "une place (feminine)"),
        (r"un\s+plat\s+favori.*couscous.*je", "le couscous (masculine)"),
    ]
    for pattern, note in gender_errors:
        if re.search(pattern, text_lower):
            errors.append(("agreement", 0.10))
    
    # Calculate score based on error penalties
    base_score = 0.9
    penalty = sum(amt for _, amt in errors)
    
    # Presence of verb conjugations (positive indicator)
    has_conjugations = any(re.search(p, text_lower) for p in [
        r"\b(suis|es|est|sommes|êtes|sont)\b",
        r"\b(ai|as|a|avons|avez|ont)\b",
        r"\b[a-z]+ais\b",
        r"\b[a-z]+é[e]?s?\b",
    ])
    
    if has_conjugations:
        base_score = 0.85
    
    return max(0.3, min(0.95, base_score - penalty))


def score_coherence_fr(
    response_text: str,
    word_count: int,
    text_lower: str,
) -> float:
    """Evalúa coherencia específica para francés."""
    connector_count = sum(
        1 for connectors in FRENCH_CONNECTORS_BY_LEVEL.values()
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


def score_sociolinguistic_fr(text_lower: str) -> float:
    """Evalúa adecuación sociolingüística en francés."""
    original_words = text_lower.split()
    
    if len(original_words) < 5:
        return 0.4
    
    score = 0.65
    
    # Check for politeness markers
    has_politeness = any(marker in text_lower for marker in FRENCH_POLITENESS_MARKERS)
    if has_politeness:
        score = 0.80
    
    # Check for informal markers
    informal_count = sum(
        1 for pattern in FRENCH_INFORMAL_MARKERS.keys() 
        if pattern in text_lower
    )
    if informal_count > 2:
        score = max(0.45, score - informal_count * 0.08)
    
    # Check for formal signals
    if any(sig in text_lower for sig in FRENCH_FORMAL_SIGNALS):
        score = min(0.90, score + 0.10)
    
    return min(1.0, score)


def score_lexicon_fr(text_lower: str, word_count: int) -> float:
    """Evalúa vocabulario con penalizaciones por errores ortográficos en francés."""
    if word_count < 5:
        return 0.2

    words = text_lower.split()
    
    common_words = {
        "le", "la", "les", "un", "une", "des", "est", "sont", "être", "eu",
        "et", "ou", "mais", "ne", "non", "pas", "je", "tu", "il", "elle",
        "nous", "vous", "ils", "elles", "quoi", "quel", "qui", "où", "quand", "comment",
    }
    
    content_words = [w for w in words if w not in common_words and len(w) > 2]
    unique_words = len(set(content_words))
    content_count = len(content_words)
    
    diversity = unique_words / content_count if content_count > 0 else 0
    
    if diversity > 0.7:
        diversity_score = 0.80
    elif diversity > 0.5:
        diversity_score = 0.60
    elif diversity > 0.3:
        diversity_score = 0.40
    else:
        diversity_score = 0.20
    
    # Penalize spelling errors
    error_penalty = sum(
        penalty for err_word, (_, penalty) in FRENCH_SPELLING_ERRORS.items()
        if err_word in text_lower
    )
    
    final_score = diversity_score - error_penalty
    return max(0.2, min(1.0, final_score))
