# 🎙️ Voice-Based Concept Understanding Analyser (VBCUA)

An AI-powered Streamlit application that evaluates how effectively users
understand and explain conceptual topics through spoken communication.
It combines **speech-to-text transcription (Whisper)**, **semantic
similarity analysis (Sentence-BERT)**, **audio feature extraction
(Librosa)**, and **automated PDF reporting (ReportLab)**.

---

## 📁 Project Structure

```
VBCUA/
├── app.py                     # Streamlit front-end & main app logic
├── audio_utils.py              # Audio loading, waveform, feature extraction
├── speech_to_text.py           # Whisper-based transcription
├── semantic_eval.py            # Sentence-BERT semantic similarity
├── scoring_engine.py           # Scoring & feedback generation
├── report_generator.py         # PDF report generation (ReportLab)
├── reference_data/
│   └── reference_concepts.py   # Predefined reference concept texts
├── test_vbcua.py                # Pytest test suite
├── requirements.txt
└── README.md
```

---

## 🖥️ System Requirements

- **OS:** Windows / Linux / macOS
- **Python:** 3.10+
- **RAM:** 4GB minimum (8GB recommended)
- **Disk:** 10GB free (Whisper + SBERT model downloads)
- Internet connection (first run downloads AI models)
- **FFmpeg** installed and available on PATH (required by Whisper)

### Installing FFmpeg
- **Windows:** `choco install ffmpeg` (or download from ffmpeg.org and add to PATH)
- **macOS:** `brew install ffmpeg`
- **Linux:** `sudo apt-get install ffmpeg`

---

## 🚀 Setup & Run Instructions (VS Code)

Open the project folder `VBCUA` in VS Code, open a terminal (`` Ctrl+` ``), then run:

### 1. Create and activate a virtual environment

**Windows:**
```bash
python -m venv vbcu_env
vbcu_env\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv vbcu_env
source vbcu_env/bin/activate
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> ⚠️ First install may take several minutes (Torch + Whisper + Sentence-Transformers are large packages).

### 3. Run the tests (optional but recommended)

```bash
pytest test_vbcua.py -v
```

### 4. Launch the Streamlit application

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 🧭 How to Use

1. **Select a Concept** — Choose a topic (e.g., "Machine Learning", "Cloud Computing") from the dropdown.
2. **Upload Audio** — Upload a `.wav` recording of you explaining the concept.
3. **Analyze** — Click "Analyze Explanation" to run transcription, semantic comparison, and audio analysis.
4. **Review Results** — View your final score, semantic similarity, fluency score, transcript, waveform, and qualitative feedback.
5. **Download Report** — Click "Download PDF Report" to save a structured report for future review.

---

## 🔧 Notes & Tips

- The first time you run the app, Whisper and Sentence-BERT will download their models automatically (requires internet). Subsequent runs use cached models.
- Use the **tiny** or **base** Whisper model for faster processing on CPU-only machines.
- Only `.wav` audio files are supported out of the box. Convert other formats using ffmpeg:
  ```bash
  ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav
  ```
- If you see `RuntimeError: openai-whisper is not installed`, ensure your virtual environment is activated and dependencies are installed.

---

## 🧩 Adding New Reference Concepts

Edit `reference_data/reference_concepts.py` and add a new entry to the `REFERENCE_CONCEPTS` dictionary:

```python
REFERENCE_CONCEPTS["Your Concept"] = "Your canonical explanation text here."
```

---

## 📜 License

This project is provided for educational purposes as part of the VBCUA capstone project.
