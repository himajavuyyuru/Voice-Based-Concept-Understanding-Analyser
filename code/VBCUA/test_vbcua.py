"""
test_vbcua.py
-------------
Basic functional tests for the scoring engine and reference data
modules (do not require audio files or model downloads).
"""

from reference_data.reference_concepts import get_concept_names, get_reference_text
from scoring_engine import (
    compute_filler_word_ratio, compute_fluency_score,
    compute_final_score, classify_final_score, run_full_evaluation
)


def test_reference_concepts_loaded():
    names = get_concept_names()
    assert "Machine Learning" in names
    assert len(get_reference_text("Machine Learning")) > 0


def test_filler_word_ratio_basic():
    text = "So, um, machine learning is like, uh, a type of AI."
    count, total, ratio = compute_filler_word_ratio(text)
    assert count >= 3
    assert total > 0
    assert 0 <= ratio <= 1


def test_filler_word_ratio_empty():
    count, total, ratio = compute_filler_word_ratio("")
    assert count == 0
    assert total == 0
    assert ratio == 0.0


def test_fluency_score_range():
    score = compute_fluency_score(filler_ratio=0.05, pause_ratio=0.2, rms_energy=0.05)
    assert 0.0 <= score <= 1.0


def test_final_score_and_classification():
    final_score = compute_final_score(semantic_similarity=0.9, fluency_score=0.8)
    assert 0 <= final_score <= 100
    classification = classify_final_score(final_score)
    assert classification in ["Strong Understanding", "Moderate Understanding", "Poor Understanding"]


def test_run_full_evaluation_pipeline():
    result = run_full_evaluation(
        semantic_similarity=0.8,
        text="Machine learning is a subset of AI that learns from data.",
        pause_ratio=0.15,
        rms_energy=0.06,
    )
    assert "final_score" in result
    assert "classification" in result
    assert isinstance(result["feedback"], list)
    assert len(result["feedback"]) > 0
