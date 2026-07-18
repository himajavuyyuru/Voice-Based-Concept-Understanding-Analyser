"""
audio_utils.py
--------------
Audio loading, waveform visualization, and feature extraction
(pause ratio, RMS energy) using Librosa and SoundFile.
"""

import io
import numpy as np
import librosa
import soundfile as sf
import matplotlib.pyplot as plt


def load_audio(file_path: str, sr: int = 16000):
    """
    Load an audio file and return the signal and sample rate.
    """
    y, sample_rate = librosa.load(file_path, sr=sr, mono=True)
    return y, sample_rate


def get_waveform_figure(y: np.ndarray, sr: int, title: str = "Waveform"):
    """
    Generate a matplotlib waveform figure for the given audio signal.
    """
    fig, ax = plt.subplots(figsize=(10, 3))
    times = np.linspace(0, len(y) / sr, num=len(y))
    ax.plot(times, y, color="#4C72B0", linewidth=0.7)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title(title)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def compute_rms_energy(y: np.ndarray) -> float:
    """
    Compute mean RMS (root mean square) energy of the audio signal.
    Higher RMS generally correlates with louder / more confident delivery.
    """
    rms = librosa.feature.rms(y=y)[0]
    return float(np.mean(rms))


def compute_pause_ratio(y: np.ndarray, sr: int, top_db: int = 30) -> float:
    """
    Estimate the pause ratio: proportion of the audio duration that is
    silence/pauses, based on librosa's silence-split intervals.
    """
    intervals = librosa.effects.split(y, top_db=top_db)
    if len(intervals) == 0:
        return 1.0  # entire clip is silence

    voiced_duration = sum((end - start) for start, end in intervals) / sr
    total_duration = len(y) / sr
    if total_duration == 0:
        return 0.0

    pause_duration = max(total_duration - voiced_duration, 0.0)
    pause_ratio = pause_duration / total_duration
    return float(np.clip(pause_ratio, 0.0, 1.0))


def get_audio_duration(y: np.ndarray, sr: int) -> float:
    return float(len(y) / sr)


def extract_audio_features(file_path: str) -> dict:
    """
    High-level convenience function: loads audio and extracts all
    relevant features in one call.
    """
    y, sr = load_audio(file_path)
    return {
        "signal": y,
        "sample_rate": sr,
        "duration": get_audio_duration(y, sr),
        "rms_energy": compute_rms_energy(y),
        "pause_ratio": compute_pause_ratio(y, sr),
    }


def figure_to_png_bytes(fig) -> bytes:
    """
    Convert a matplotlib figure to PNG bytes (useful for embedding
    into PDF reports).
    """
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    return buf.read()
