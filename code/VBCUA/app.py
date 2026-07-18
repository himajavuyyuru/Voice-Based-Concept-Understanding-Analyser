"""
app.py
------
Voice-Based Concept Understanding Analyser (VBCUA)
Streamlit front-end and main application logic.

Run with:
    streamlit run app.py
"""

import os
import tempfile
import streamlit as st

from reference_data.reference_concepts import get_concept_names, get_reference_text
from audio_utils import (
    load_audio, get_waveform_figure, compute_rms_energy,
    compute_pause_ratio, get_audio_duration, figure_to_png_bytes
)
from speech_to_text import transcribe_audio
from semantic_eval import compute_semantic_similarity
from scoring_engine import run_full_evaluation
from report_generator import generate_pdf_report


# ----------------------------------------------------------------------
# Page configuration
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="VBCUA - Voice-Based Concept Understanding Analyser",
    page_icon="🎙️",
    layout="wide",
)

# ----------------------------------------------------------------------
# Session state initialization
# ----------------------------------------------------------------------
for key, default in {
    "transcript": None,
    "audio_features": None,
    "waveform_png": None,
    "evaluation_result": None,
    "concept": None,
    "audio_path": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ----------------------------------------------------------------------
# Sidebar - configuration
# ----------------------------------------------------------------------
st.sidebar.title("⚙️ Settings")
whisper_model_size = st.sidebar.selectbox(
    "Whisper Model Size",
    ["tiny", "base", "small"],
    index=1,
    help="Larger models are more accurate but slower to load."
)
st.sidebar.markdown("---")
st.sidebar.markdown(
    "**VBCUA** combines Whisper transcription, Sentence-BERT semantic "
    "similarity, and Librosa audio analysis to evaluate spoken conceptual "
    "explanations."
)

# ----------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------
st.title("🎙️ Voice-Based Concept Understanding Analyser (VBCUA)")
st.caption(
    "Evaluate how effectively you understand and explain conceptual "
    "topics through spoken communication."
)

# ----------------------------------------------------------------------
# Step 1: Select reference concept
# ----------------------------------------------------------------------
st.header("1️⃣ Select a Concept")
concept = st.selectbox("Choose the concept you will explain:", get_concept_names())
with st.expander("View reference explanation"):
    st.write(get_reference_text(concept))

# ----------------------------------------------------------------------
# Step 2: Upload audio
# ----------------------------------------------------------------------
st.header("2️⃣ Upload Your Spoken Explanation")
audio_file = st.file_uploader("Upload a WAV audio file", type=["wav"])

if audio_file is not None:
    st.audio(audio_file, format="audio/wav")

    if st.button("🔍 Analyze Explanation", type="primary"):
        with st.spinner("Processing audio and running analysis..."):
            # Save uploaded file to a temp path
            temp_dir = tempfile.mkdtemp()
            audio_path = os.path.join(temp_dir, "input.wav")
            with open(audio_path, "wb") as f:
                f.write(audio_file.getbuffer())
            st.session_state.audio_path = audio_path

            # --- Audio feature extraction ---
            y, sr = load_audio(audio_path)
            duration = get_audio_duration(y, sr)
            rms_energy = compute_rms_energy(y)
            pause_ratio = compute_pause_ratio(y, sr)

            fig = get_waveform_figure(y, sr, title=f"Waveform - {concept}")
            waveform_png = figure_to_png_bytes(fig)

            st.session_state.audio_features = {
                "duration": duration,
                "rms_energy": rms_energy,
                "pause_ratio": pause_ratio,
            }
            st.session_state.waveform_png = waveform_png

            # --- Speech to text ---
            try:
                transcription = transcribe_audio(audio_path, model_size=whisper_model_size)
                transcript_text = transcription["text"]
            except Exception as e:
                st.error(f"Transcription failed: {e}")
                transcript_text = ""
            st.session_state.transcript = transcript_text

            # --- Semantic similarity ---
            reference_text = get_reference_text(concept)
            try:
                similarity = compute_semantic_similarity(transcript_text, reference_text)
            except Exception as e:
                st.error(f"Semantic evaluation failed: {e}")
                similarity = 0.0

            # --- Final scoring ---
            result = run_full_evaluation(
                semantic_similarity=similarity,
                text=transcript_text,
                pause_ratio=pause_ratio,
                rms_energy=rms_energy,
            )
            st.session_state.evaluation_result = result
            st.session_state.concept = concept

        st.success("Analysis complete!")

# ----------------------------------------------------------------------
# Step 3: Display results
# ----------------------------------------------------------------------
if st.session_state.evaluation_result is not None:
    st.header("3️⃣ Evaluation Results")

    result = st.session_state.evaluation_result
    features = st.session_state.audio_features

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Final Score", f"{result['final_score']}%")
    col2.metric("Semantic Similarity", f"{result['semantic_similarity']}%")
    col3.metric("Fluency Score", f"{result['fluency_score']}%")
    col4.metric("Classification", result["classification"])

    st.subheader("📝 Transcribed Explanation")
    st.write(st.session_state.transcript or "_No speech detected._")

    st.subheader("📊 Waveform Visualization")
    if st.session_state.audio_path:
        y, sr = load_audio(st.session_state.audio_path)
        fig = get_waveform_figure(y, sr, title=f"Waveform - {st.session_state.concept}")
        st.pyplot(fig)

    st.subheader("🔎 Detailed Metrics")
    metrics_col1, metrics_col2 = st.columns(2)
    with metrics_col1:
        st.write(f"**Filler Words:** {result['filler_count']} / {result['total_words']} words "
                  f"({result['filler_ratio']}%)")
        st.write(f"**Pause Ratio:** {result['pause_ratio']}%")
    with metrics_col2:
        st.write(f"**RMS Energy:** {result['rms_energy']}")
        st.write(f"**Audio Duration:** {features['duration']:.2f} seconds")

    st.subheader("💡 Qualitative Feedback")
    for point in result["feedback"]:
        st.markdown(f"- {point}")

    # ------------------------------------------------------------------
    # Step 4: PDF report download
    # ------------------------------------------------------------------
    st.header("4️⃣ Download Report")
    pdf_bytes = generate_pdf_report(
        concept_name=st.session_state.concept,
        transcript=st.session_state.transcript or "",
        result=result,
        waveform_png_bytes=st.session_state.waveform_png,
    )
    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_bytes,
        file_name=f"VBCUA_Report_{st.session_state.concept.replace(' ', '_')}.pdf",
        mime="application/pdf",
    )
else:
    st.info("Upload a WAV audio file and click 'Analyze Explanation' to see results here.")
