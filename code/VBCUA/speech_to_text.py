"""
speech_to_text.py
------------------
Whisper-based transcription logic for the VBCUA project.
Handles loading the Whisper model (cached) and transcribing WAV audio
files into text.
"""

import os
import streamlit as st

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False


@st.cache_resource(show_spinner=False)
def load_whisper_model(model_size: str = "base"):
    """
    Load and cache the Whisper model so it is not reloaded on every run.
    """
    if not WHISPER_AVAILABLE:
        raise RuntimeError(
            "openai-whisper is not installed. Run: pip install openai-whisper"
        )
    model = whisper.load_model(model_size)
    return model


def transcribe_audio(file_path: str, model_size: str = "base") -> dict:
    """
    Transcribe an audio file using Whisper.

    Returns a dict with keys: 'text', 'language', 'segments'
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    model = load_whisper_model(model_size)
    result = model.transcribe(file_path, fp16=False)

    return {
        "text": result.get("text", "").strip(),
        "language": result.get("language", "unknown"),
        "segments": result.get("segments", []),
    }
