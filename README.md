#  Voice-Based Concept Understanding Assessment

VBCUA is an AI-powered system that evaluates a speaker's understanding of a concept from a spoken (audio) explanation. It combines **speech-to-text transcription**, **semantic similarity analysis**, and **audio feature extraction** to generate an objective "understanding score" along with a downloadable PDF report.
## Overview

VBCUA is built with Python and modern AI/ML libraries for speech processing, semantic analysis, web application development, and report generation. The system takes an uploaded audio explanation, transcribes it, compares it semantically against a reference concept, analyzes speech-quality signals (pauses, energy, filler words), and produces a final classification: **Strong**, **Moderate**, or **Poor** understanding.

**Core capabilities:**
- Speech-to-text transcription using OpenAI Whisper
- Semantic similarity scoring using Sentence-BERT
- Audio feature extraction (pause ratio, RMS energy) using Librosa/SoundFile
- Filler word detection from transcribed text
- Combined scoring engine for a final understanding score
- Interactive Streamlit UI with waveform visualization
- Automated PDF report generation using ReportLab

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| Web/UI Framework | Streamlit |
| API Framework | FastAPI |
| Speech-to-Text | OpenAI Whisper |
| Semantic Similarity | Sentence-BERT |
| Audio Processing | Librosa, SoundFile |
| Visualization | Matplotlib |
| Report Generation | ReportLab |
| NLP Utilities | NLTK |
| IDE | Visual Studio Code |

---

## Project Structure

The project follows a modular structure to keep UI, audio processing, NLP evaluation, and reporting cleanly separated:

```
VBCUA/
├── app.py                  # Streamlit front-end and main application logic
├── audio_utils.py          # Audio loading and feature extraction utilities
├── speech_to_text.py       # Whisper-based transcription logic
├── semantic_eval.py        # Semantic similarity computation using Sentence-BERT
├── scoring_engine.py       # Understanding score calculation and classification
├── report_generator.py     # PDF report generation using ReportLab
├── requirements.txt        # Project dependencies
└── README.md
```

---

## How It Works

1. **Audio Input** – User uploads a WAV audio file explaining a concept via the Streamlit UI.
2. **Transcription** – `speech_to_text.py` uses Whisper to convert the audio into text.
3. **Semantic Evaluation** – `semantic_eval.py` generates Sentence-BERT embeddings for the transcription and the reference concept, then computes cosine similarity.
4. **Audio Feature Extraction** – `audio_utils.py` extracts pause ratio and RMS energy using Librosa/SoundFile.
5. **Filler Word Detection** – Filler word ratio is computed from the transcribed text.
6. **Scoring** – `scoring_engine.py` combines semantic similarity, filler usage, and audio confidence metrics into a final understanding score and classification (Strong / Moderate / Poor).
7. **Reporting** – `report_generator.py` produces a downloadable PDF report summarizing the results.
8. **UI Presentation** – `app.py` renders reference concepts, waveform visualization, evaluation metrics, and final results in a clean, responsive Streamlit layout.

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

1. **Clone the repository**
   ```bash
  https://github.com/himajavuyyuru/Voice-Based-Concept-Understanding-Analyser.git

2. **Create and activate a virtual environment**
   ```bash
   python -m venv vbcu_env

   # Windows
   vbcu_env\Scripts\activate

   # macOS/Linux
   source vbcu_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   `requirements.txt` should include (at minimum):
   ```
   streamlit
   openai-whisper
   sentence-transformers
   librosa
   soundfile
   matplotlib
   reportlab
   nltk
   fastapi
   ```

4. **Verify the installation**
   Confirm all modules import correctly and that core components (transcription, semantic similarity, audio feature extraction, UI rendering) run without errors.

---

## Usage

Launch the application with:

```bash
streamlit run app.py
```

Then, in the browser UI:
1. Select or enter the reference concept.
2. Upload a WAV audio file containing the spoken explanation.
3. Review the automatically generated waveform, transcription, and evaluation metrics.
4. View the final understanding score and classification.
5. Download the generated PDF report.

---

## Testing

- Validate audio uploads, transcription accuracy, waveform rendering, and metric computation.
- Test across varied speech styles, accents, and recording qualities.
- Verify semantic similarity scoring, filler word detection, and scoring consistency across multiple test samples.
- Confirm end-to-end flow: audio input → transcription → analysis → scoring → PDF output.

---

## Performance Optimization

- Model loading is cached using Streamlit's caching utilities to reduce latency on repeated runs.
- Runtime performance is measured for transcription, embedding computation, and audio feature extraction.
- The system is validated for stability under repeated evaluations and longer audio inputs.

---

## Deployment

- Supports deployment on local systems or Streamlit Cloud.
- Final end-to-end testing covers the complete pipeline: audio input → analysis → evaluation → PDF output.
- Includes logging, error handling, and safe fallback mechanisms prior to release.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
