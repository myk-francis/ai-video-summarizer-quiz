# scorer.py

import re
import math
from collections import Counter

# --- Lexicons (can be expanded) ---

EMOTION_WORDS = {
    "fear", "love", "hate", "anger", "shame", "hope", "joy",
    "anxiety", "panic", "sad", "happy", "excited", "terrified"
}

INSIGHT_WORDS = {
    "realized", "learned", "understood", "noticed",
    "figured", "discovered", "recognized"
}

Cliches = {
    "at the end of the day",
    "everything happens for a reason",
    "you just have to",
    "believe in yourself",
    "trust the process"
}

UNCERTAINTY_MARKERS = {
    "i don't know", "maybe", "i think", "i guess",
    "i'm not sure", "kind of", "sort of"
}

CONTRAST_MARKERS = {"but", "however", "until", "suddenly", "then"}

STAKE_WORDS = {"risk", "lose", "lost", "failure", "consequence", "death"}

FIRST_PERSON = {"i", "me", "my", "we", "our"}

# --- Helpers ---

def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())

def count_phrases(text, phrases):
    return sum(1 for p in phrases if p in text.lower())

# --- Metric Calculations ---

def resonance_density(text, duration_sec):
    words = tokenize(text)
    emotion = sum(1 for w in words if w in EMOTION_WORDS)
    insight = sum(1 for w in words if w in INSIGHT_WORDS)

    # crude sentiment variance proxy
    sentiment_variance = abs(emotion - insight)

    if duration_sec == 0:
        return 0

    return (emotion * 1.5 + insight * 1.2 + sentiment_variance * 10) / duration_sec


def quotability_score(text):
    sentences = re.split(r"[.!?]", text)
    short_sentences = sum(1 for s in sentences if 20 < len(s) < 140)
    declarative = sum(1 for s in sentences if s.strip().endswith(""))
    first_person = sum(
        1 for w in tokenize(text) if w in FIRST_PERSON
    )

    return short_sentences * 2.0 + declarative * 1.5 + first_person * 1.2


def narrative_turn_score(text):
    tokens = tokenize(text)
    contrast = sum(1 for w in tokens if w in CONTRAST_MARKERS)
    stakes = sum(1 for w in tokens if w in STAKE_WORDS)

    belief_reversal = count_phrases(
        text,
        ["used to think", "thought that", "but then", "until i realized"]
    )

    return contrast * 2.0 + belief_reversal * 3.0 + stakes * 1.5


def human_provenance_score(text):
    tokens = tokenize(text)
    first_person = sum(1 for w in tokens if w in FIRST_PERSON)
    uncertainty = count_phrases(text, UNCERTAINTY_MARKERS)

    specificity = sum(
        1 for w in tokens if w.isdigit()
    )

    return (
        first_person * 1.5 +
        uncertainty * 2.0 +
        specificity * 2.5
    )


def slop_penalty(text):
    cliché_count = count_phrases(text, Cliches)
    generic_motivation = count_phrases(
        text,
        ["success", "mindset", "grind", "motivation"]
    )

    return cliché_count * 3.0 + generic_motivation * 2.0


# --- Final Composite ---

def narrative_liquidity(text, duration_sec):
    r = resonance_density(text, duration_sec)
    q = quotability_score(text)
    n = narrative_turn_score(text)
    h = human_provenance_score(text)
    s = slop_penalty(text)

    score = (
        r * 0.25 +
        q * 0.20 +
        n * 0.25 +
        h * 0.30
    ) - s

    return max(0, min(100, round(score, 2)))
