"""
Environment and Dependency Verification Script.
Checks Python version, installed AI libraries, and media processing capabilities.
"""

import sys
import shutil
from pathlib import Path

def check_env():
    print("=" * 60)
    print(" GENAI VIDEO INTELLIGENCE STUDIO — ENVIRONMENT CHECK")
    print("=" * 60)
    print(f"Python Version: {sys.version.split()[0]} ({sys.platform})")

    required_modules = [
        ("gradio", "Gradio UI Framework"),
        ("ollama", "Ollama Python Client"),
        ("pydantic", "Pydantic Structured Validation"),
        ("faster_whisper", "faster-whisper Speech Recognition"),
        ("edge_tts", "edge-tts Multilingual Neural Speech"),
        ("pyttsx3", "pyttsx3 Offline TTS Engine"),
        ("cv2", "OpenCV Computer Vision"),
        ("PIL", "Pillow Image Processing"),
        ("reportlab", "ReportLab PDF Generation"),
        ("fitz", "PyMuPDF PDF Preview Rendering"),
        ("pandas", "Pandas Data Analytics"),
        ("plotly", "Plotly Interactive Visualizations"),
        ("yt_dlp", "yt-dlp Video Metadata Extractor")
    ]

    all_passed = True
    for mod_name, label in required_modules:
        try:
            mod = __import__(mod_name)
            ver = getattr(mod, "__version__", "Installed")
            print(f"  [PASS] {label:35s}: {ver}")
        except ImportError as e:
            print(f"  [FAIL] {label:35s}: MISSING ({e})")
            all_passed = False

    print("-" * 60)
    # Check static_ffmpeg
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
        print("  [PASS] static_ffmpeg binaries initialized successfully.")
    except Exception as e:
        print(f"  [WARN] static_ffmpeg: {e}")

    ffmpeg_bin = shutil.which("ffmpeg")
    ffprobe_bin = shutil.which("ffprobe")
    print(f"  FFmpeg in PATH:  {'YES' if ffmpeg_bin else 'NO'} ({ffmpeg_bin})")
    print(f"  FFprobe in PATH: {'YES' if ffprobe_bin else 'NO'} ({ffprobe_bin})")
    print("=" * 60)

    return all_passed

if __name__ == "__main__":
    check_env()
