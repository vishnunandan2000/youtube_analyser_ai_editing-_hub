# 🚀 GenAI Video Intelligence Studio

An enterprise-grade, modular, production-ready AI application combining YouTube performance analytics with autonomous educational video editing, multilingual captions and dubbing, motion graphics, and content generation.

---

## 🌟 Executive Overview

**GenAI Video Intelligence Studio** is architected into two primary divisions:

### 📊 DIVISION A — YouTube Intelligence & Performance Analytics
- **Video Metadata & Snapshot Extraction**: Public view counts, likes, comments, duration, publication date, thumbnail, tags, and channel info.
- **Analytics KPIs**: Public metrics (views, likes, comments), calculated engagement rates (like-to-view ratio, comment-to-view ratio, public engagement rate), and clearly demarcated authenticated channel analytics (shares, subscribers gained, retention metrics).
- **Interactive Visualizations**: Plotly sentiment distribution donut charts, comment volume bar charts, and logarithmic reach scale charts.
- **Comment Collection & Sentiment Classification**: Scrapes top comments, clusters into **Positive**, **Negative**, and **Neutral** categories with reasoning, topic identification, and actionable feedback flags powered by local `llama3.2:latest`.
- **Audience Feedback Synthesis**: Highlights recurring clarification requests, positive highlights, technical bug reports, and pedagogical suggestions.
- **AI Content Improvement Copilot**: Conversational AI assistant aware of video metrics, transcripts, and audience sentiment, featuring one-click actions for high-converting titles, 15-second retention hooks, thumbnail concepts, and video chapter outlines.

### 🎬 DIVISION B — Autonomous Video Production Studio
- **Autonomous Multi-Agent Editing Pipeline**: Inspects media via FFprobe, extracts audio, detects visual scene transitions via OpenCV, transcribes speech with `faster-whisper`, and generates structured Edit Decision Lists (EDL) using `llama3.2:latest`.
- **Conservative Educational Cutting**: Trims dead pauses while strictly preserving equations, code demos, and teacher explanations without destructive cuts.
- **Multilingual Captions & Synchronized Dubbing**: Translates and synchronizes subtitles across **12 languages** (*English, Hindi, Telugu, Tamil, Kannada, Malayalam, Marathi, Bengali, Spanish, French, German, Japanese*) with technical term preservation. Synthesizes voice dubbing via `edge-tts` (with `pyttsx3` offline fallback) and audio ducking.
- **Context-Aware Educational Motion Graphics**: Generates procedural 2D visual animations (Machine Learning Pipeline, Deep Learning Neural Network, Cybersecurity Packet Filter, Concept Cards) guided by pedagogical motion graphics principles.
- **AI Thumbnail Generator**: Produces 3 distinct 1280×720 thumbnail designs (*High-Impact Cyber Tech*, *Minimalist Executive*, *High-Energy Explainer*) with custom instructor photo / logo compositing.
- **Handwritten Study Notes PDF**: Converts speech transcripts into structured A4 PDF study guides with notebook ruled margins, definitions, code blocks, revision questions, and high-res page image previews.
- **Autonomous YouTube Shorts Generator**: Reframes video into 1080×1920 (9:16 vertical) with blurred background padding and kinetic captions, strictly enforcing a duration $\le 60$ seconds.
- **Like, Share, Comment & Subscribe Studio**: Produces animated lower-third overlays featuring channel name, subscriber count, bell chime, and button click animations.
- **Export Center & Quality Assurance**: Validates and serves all generated assets (*Edited MP4, Captioned MP4, Dubbed MP4, SRT, VTT, Thumbnail PNGs, Notes PDF, Shorts MP4*).

---

## 🛠️ Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **User Interface** | Gradio 6.27 Blocks | Responsive SaaS dashboard with 12 distinct tabs |
| **Language Model** | Ollama (`llama3.2:latest`) | Local reasoning, structured JSON parsing, Copilot |
| **Speech-to-Text** | `faster-whisper` (1.2.1) | Timestamped sentence and word-level speech recognition |
| **Text-to-Speech** | `edge-tts` (7.2.8) + `pyttsx3` | Multilingual neural voiceover with offline SAPI5 fallback |
| **Video Automation** | FFmpeg 8.0.1 + `static-ffmpeg` | Audio extraction, cutting, subtitle burning, concat |
| **Computer Vision** | OpenCV (`cv2` 5.0.0) | Frame differencing, scene transition detection |
| **Image & Graphics** | Pillow (10.3.0) | Thumbnails, procedural motion graphic frames |
| **Document Engine** | ReportLab 4.2 + PyMuPDF | A4 PDF study notes and page preview rendering |
| **Data & Charts** | Pandas 2.2 + Plotly 7.0 | Analytics calculations and responsive charts |
| **Job Queue & DB** | SQLite + ThreadPoolExecutor | Background task management and progress logging |
| **Test Suite** | pytest 9.0 | Automated unit and integration tests |

---

## 📋 Directory Architecture

```
youtube_edit_ai_hub/
├── app.py                     # Main application entrypoint
├── config.py                  # Pydantic environment configuration
├── requirements.txt           # Python package dependencies
├── .env.example               # Environment variables template
├── README.md                  # Comprehensive documentation
├── agents/                    # Multi-Agent Orchestration Layer
│   ├── orchestrator.py        # Master production pipeline coordinator
│   ├── youtube_analytics_agent.py # Division A analytics & charts
│   ├── sentiment_agent.py     # Comment classification & topic clustering
│   ├── content_strategy_agent.py # Copilot chatbot & creative actions
│   ├── speech_agent.py        # Speech extraction & transcription
│   ├── video_understanding_agent.py # Scene detection & keyframing
│   ├── editing_agent.py       # EDL synthesis & safe video cutting
│   ├── translation_agent.py   # Subtitle translation (12 languages)
│   ├── tts_agent.py           # Neural voice dubbing & audio ducking
│   ├── animation_agent.py     # Educational motion graphics
│   ├── thumbnail_agent.py     # AI thumbnail generation
│   ├── notes_agent.py         # Study notes PDF synthesis
│   ├── shorts_agent.py        # YouTube Shorts extraction (<=60s)
│   └── quality_agent.py       # Quality assurance & verification
├── services/                  # Business Logic & External Engines
│   ├── ollama_service.py      # Ollama client, health check, JSON repair
│   ├── youtube_service.py     # YouTube Data API v3 & yt-dlp fallback
│   ├── oauth_service.py       # OAuth 2.0 analytics authentication
│   ├── transcription_service.py # faster-whisper transcription & SRT/VTT
│   ├── translation_service.py # Multilingual translation preserving terms
│   ├── tts_service.py         # edge-tts and pyttsx3 speech dubbing
│   ├── video_service.py       # FFmpeg media probe, scene cuts, subtitles
│   ├── animation_service.py   # Procedural motion graphics rendering
│   ├── thumbnail_service.py   # Pillow 1280x720 thumbnail designs
│   ├── notes_service.py       # ReportLab PDF & PyMuPDF image renderer
│   ├── shorts_service.py      # 9:16 vertical video & duration checks
│   └── storage_service.py     # Thread-safe job queue & SQLite persistence
├── ui/                        # Gradio Blocks Presentation Layer
│   ├── styles.py              # CSS design tokens & theme classes
│   ├── dashboard.py           # Overview Dashboard tab
│   ├── youtube_tab.py         # YouTube Intelligence tab
│   ├── video_editor_tab.py    # Automatic Video Editor tab
│   ├── captions_tab.py        # Multilingual Captions & Dubbing tab
│   ├── animation_tab.py       # Animation Studio tab
│   ├── thumbnail_tab.py       # AI Thumbnail Generator tab
│   ├── notes_tab.py           # Handwritten Study Notes tab
│   ├── shorts_tab.py          # YouTube Shorts Generator tab
│   ├── lss_tab.py             # Like, Share & Subscribe tab
│   ├── chatbot_tab.py         # AI Content Improvement Chatbot tab
│   ├── export_tab.py          # Export Center tab
│   └── settings_tab.py        # Settings & System Diagnostics tab
├── models/                    # Pydantic Schemas & Data Contracts
│   ├── schemas.py             # Subtitles, transcriptions, chapters, notes
│   ├── analytics_models.py    # KPIs, comments, sentiment, improvements
│   ├── editing_models.py      # EDL, operations allowlist, animations
│   └── job_models.py          # Background jobs, stages, artifacts
├── utils/                     # Helper Utilities & Security
│   ├── logging_config.py      # Structured file & console logging
│   ├── file_validation.py     # Path traversal protection & file checks
│   ├── media_utils.py         # static-ffmpeg injection & safe subprocesses
│   ├── timestamp_utils.py     # SRT/VTT timecode math
│   └── error_handlers.py      # Custom exceptions & UI error formatting
├── data/                      # Local File Storage
│   ├── jobs/                  # Per-job processing folders
│   ├── exports/               # Rendered final deliverables
│   └── cache/                 # Temporary working files
├── tests/                     # Automated Test Suite (16 unit tests)
└── scripts/                   # Environment & Dependency Diagnostics
```

---

## ⚡ Quickstart Guide

### 1. Prerequisites
- **Python 3.11 or 3.12**
- **Ollama** installed with `llama3.2:latest`:
  ```bash
  ollama serve
  ollama run llama3.2:latest
  ```

### 2. Installation
Install project dependencies:
```bash
pip install -r requirements.txt
```

### 3. Verify Environment
Run the built-in diagnostic scripts to verify your environment, Ollama connectivity, and FFmpeg binaries:
```bash
python scripts/check_environment.py
python scripts/check_ollama.py
python scripts/check_ffmpeg.py
```

### 4. Run Automated Tests
Execute the full test suite:
```bash
pytest -v
```

### 5. Launch the Studio
Start the Gradio web application:
```bash
python app.py
```
Open your browser to: **http://127.0.0.1:7860**

---

## 🔒 Configuration & Environment Variables

Create a `.env` file in the project root (copied from `.env.example`):
```ini
# Ollama LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:latest
OLLAMA_TIMEOUT_SECONDS=60

# YouTube API Configuration (Optional - yt-dlp metadata fallback provided)
YOUTUBE_API_KEY=
YOUTUBE_CLIENT_SECRETS_FILE=

# Database & Limits
DATABASE_URL=sqlite:///data/app.db
MAX_UPLOAD_SIZE_MB=500
MAX_VIDEO_DURATION_MINUTES=60
MAX_CONCURRENT_JOBS=1
DEFAULT_OUTPUT_LANGUAGE=en
LOG_LEVEL=INFO
```

---

## 🧪 Feature Implementation & Verification Matrix

| Feature | Implementation Status | Verified Engine |
| :--- | :---: | :--- |
| **YouTube Metadata & KPIs** | ✅ Functional | `yt-dlp` + Data API v3 fallback |
| **Comment Sentiment Analysis** | ✅ Functional | Llama 3.2 (Positive/Negative/Neutral) |
| **Audience Topic Extraction** | ✅ Functional | Deterministic JSON aggregation |
| **AI Creative Copilot Chat** | ✅ Functional | Llama 3.2 interactive chat + actions |
| **Speech Transcription** | ✅ Functional | `faster-whisper` (base int8) |
| **Multilingual Subtitles** | ✅ Functional | 12 Languages (SRT + WebVTT) |
| **Synchronized Voice Dubbing** | ✅ Functional | `edge-tts` (neural) + `pyttsx3` fallback |
| **Conservative Video Cuts** | ✅ Functional | Structured EDL via FFmpeg |
| **Burned-in Captions** | ✅ Functional | FFmpeg subtitle filter |
| **Educational Motion Graphics** | ✅ Functional | Pillow + FFmpeg Alpha Compositing |
| **1280x720 AI Thumbnails** | ✅ Functional | 3 distinct Pillow design concepts |
| **A4 Handwritten Notes PDF** | ✅ Functional | ReportLab 4.2 + PyMuPDF previews |
| **YouTube Shorts ($\le$ 60s)** | ✅ Functional | 9:16 vertical reframing, duration verified |
| **Engagement Animations** | ✅ Functional | Like, Share, Subscribe lower-thirds |
| **Export Center** | ✅ Functional | Verified real file downloads |
| **Automated Test Suite** | ✅ Functional | 16 tests passing in `pytest` |
