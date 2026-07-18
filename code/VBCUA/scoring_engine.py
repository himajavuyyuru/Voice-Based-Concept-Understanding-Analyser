"""
scoring_engine.py
------------------
Combines semantic similarity, filler word usage, pause ratio, and RMS
energy into a final understanding score and qualitative classification.
"""

import re

FILLER_WORDS = [
    "um", "uh", "like", "you know", "actually", "basically",
    "literally", "so", "well", "i mean", "kind of", "sort of", "hmm",
]


def compute_filler_word_ratio(text: str) -> tuple:
    """
    Count filler words in the transcribed text and compute their ratio
    relative to total word count.

    Returns (filler_count, total_words, filler_ratio)
    """
    if not text.strip():
        return 0, 0, 0.0

    cleaned = text.lower()
    words = re.findall(r"\b[\w']+\b", cleaned)
    total_words = len(words)

    filler_count = 0
    for phrase in FILLER_WORDS:
        pattern = r"\b" + re.escape(phrase) + r"\b"
        filler_count += len(re.findall(pattern, cleaned))

    filler_ratio = filler_count / total_words if total_words > 0 else 0.0
    return filler_count, total_words, float(min(filler_ratio, 1.0))


def compute_fluency_score(filler_ratio: float, pause_ratio: float,
                           rms_energy: float) -> float:
    """
    Combine fluency-related metrics into a single fluency score in [0, 1].
    - Lower filler ratio -> better
    - Lower pause ratio -> better (up to a point; some pause is natural)
    - Moderate-to-high RMS energy -> better (clearer, more confident voice)
    """
    filler_component = max(0.0, 1 - (filler_ratio * 4))  # penalize fillers heavily
    pause_component = max(0.0, 1 - pause_ratio)

    # Normalize RMS energy loosely into [0, 1]; typical speech RMS ~0.01-0.2
    energy_component = min(rms_energy / 0.1, 1.0)

    fluency_score = (
        0.5 * filler_component +
        0.3 * pause_component +
        0.2 * energy_component
    )
    return float(max(0.0, min(fluency_score, 1.0)))


def compute_final_score(semantic_similarity: float, fluency_score: float,
                         semantic_weight: float = 0.7,
                         fluency_weight: float = 0.3) -> float:
    """
    Weighted combination of semantic understanding and speech fluency
    into a single final understanding score (0-100 scale).
    """
    combined = (semantic_similarity * semantic_weight) + (fluency_score * fluency_weight)
    return round(combined * 100, 2)


def classify_final_score(final_score: float) -> str:
    if final_score >= 75:
        return "Strong Understanding"
    elif final_score >= 50:
        return "Moderate Understanding"
    else:
        return "Poor Understanding"


def generate_feedback(semantic_similarity: float, filler_ratio: float,
                       pause_ratio: float, classification: str) -> list:
    """
    Generate a list of qualitative, human-readable feedback bullet points
    based on computed metrics.
    """
    feedback = []

    if semantic_similarity >= 0.75:
        feedback.append("Your explanation closely aligns with the core concept.")
    elif semantic_similarity >= 0.5:
        feedback.append("Your explanation captures some key ideas but misses important details.")
    else:
        feedback.append("Your explanation deviates significantly from the expected concept. Review the core definitions.")

    if filler_ratio > 0.1:
        feedback.append("High use of filler words detected — try to reduce 'um', 'like', and 'uh' for clearer delivery.")
    elif filler_ratio > 0.03:
        feedback.append("Moderate filler word usage — minor improvement could enhance fluency.")
    else:
        feedback.append("Minimal filler word usage — excellent speech clarity.")

    if pause_ratio > 0.4:
        feedback.append("Frequent pauses detected — practice speaking more continuously to build confidence.")
    elif pause_ratio > 0.2:
        feedback.append("Some natural pausing detected — generally acceptable pacing.")
    else:
        feedback.append("Good pacing with minimal unnecessary pauses.")

    feedback.append(f"Overall Classification: {classification}.")
    return feedback


def run_full_evaluation(semantic_similarity: float, text: str,
                         pause_ratio: float, rms_energy: float) -> dict:
    """
    Orchestrates the full scoring pipeline and returns a structured
    result dictionary consumed by the UI and report generator.
    """
    filler_count, total_words, filler_ratio = compute_filler_word_ratio(text)
    fluency_score = compute_fluency_score(filler_ratio, pause_ratio, rms_energy)
    final_score = compute_final_score(semantic_similarity, fluency_score)
    classification = classify_final_score(final_score)
    feedback = generate_feedback(semantic_similarity, filler_ratio, pause_ratio, classification)

    return {
        "semantic_similarity": round(semantic_similarity * 100, 2),
        "fluency_score": round(fluency_score * 100, 2),
        "final_score": final_score,
        "classification": classification,
        "filler_count": filler_count,
        "total_words": total_words,
        "filler_ratio": round(filler_ratio * 100, 2),
        "pause_ratio": round(pause_ratio * 100, 2),
        "rms_energy": round(rms_energy, 5),
        "feedback": feedback,
    }
