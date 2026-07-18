"""
semantic_eval.py
-----------------
Semantic similarity computation between a user's spoken explanation
and a predefined reference concept, using Sentence-BERT embeddings.
"""

import streamlit as st
import numpy as np

try:
    from sentence_transformers import SentenceTransformer, util
    SBERT_AVAILABLE = True
except ImportError:
    SBERT_AVAILABLE = False


@st.cache_resource(show_spinner=False)
def load_sbert_model(model_name: str = "all-MiniLM-L6-v2"):
    """
    Load and cache the Sentence-BERT model.
    """
    if not SBERT_AVAILABLE:
        raise RuntimeError(
            "sentence-transformers is not installed. "
            "Run: pip install sentence-transformers"
        )
    return SentenceTransformer(model_name)


def compute_semantic_similarity(user_text: str, reference_text: str,
                                 model_name: str = "all-MiniLM-L6-v2") -> float:
    """
    Compute cosine similarity between the embeddings of the user's
    explanation and the reference concept text. Returns a value in [0, 1].
    """
    if not user_text.strip():
        return 0.0

    model = load_sbert_model(model_name)
    embeddings = model.encode([user_text, reference_text], convert_to_tensor=True)
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()

    # Cosine similarity for SBERT embeddings can range roughly [-1, 1];
    # normalize/clip to [0, 1] for consistent scoring.
    normalized = (similarity + 1) / 2
    return float(np.clip(normalized, 0.0, 1.0))


def classify_understanding(similarity_score: float) -> str:
    """
    Convert a normalized similarity score into a qualitative label.
    """
    if similarity_score >= 0.75:
        return "Strong Understanding"
    elif similarity_score >= 0.5:
        return "Moderate Understanding"
    else:
        return "Poor Understanding"
