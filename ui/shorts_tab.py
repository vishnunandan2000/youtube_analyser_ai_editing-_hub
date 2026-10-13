"""
YouTube Shorts Generator Tab.
"""

import gradio as gr
from pathlib import Path
from agents.shorts_agent import shorts_agent
from services.transcription_service import transcription_service
from services.video_service import video_service
from config import settings
from utils.error_handlers import format_error_for_ui

def create_shorts_tab():
    with gr.Tab("YouTube Shorts Generator", id="tab_shorts"):
        gr.Markdown("## 📱 Autonomous YouTube Shorts Generator (1080 × 1920 Vertical)")
        gr.Markdown("Extracts self-contained educational highlights, reframes to 9:16 vertical video, and strictly enforces duration constraints (≤60 seconds).")

        with gr.Row():
            with gr.Column(scale=1):
                video_file = gr.Video(label="Upload Long-Form Lecture Video", sources=["upload"])
                load_shorts_sample_btn = gr.Button("🎬 Load Sample Educational Video", variant="secondary", size="sm")
                hook_override = gr.Textbox(label="Custom Opening Hook Banner", value="MASTER THIS IN 60 SECONDS!")
                cta_override = gr.Textbox(label="Closing Call To Action", value="SUBSCRIBE FOR DAILY AI INSIGHTS!")
                generate_shorts_btn = gr.Button("✂️ Generate Vertical Short (≤60s)", variant="primary", elem_classes=["action-btn-primary"])

            with gr.Column(scale=1):
                short_video_player = gr.Video(label="Vertical Short Video Preview (9:16)", height=450)
                download_short_file = gr.File(label="Download Rendered MP4 Short")

        candidate_info_box = gr.Markdown("Ready to extract Shorts. Upload a video file.")

        def handle_shorts_extraction(v_file, hook, cta):
            if not v_file:
                return "⚠️ Please upload a video file first.", None, None
            try:
                p = Path(v_file)
                meta = video_service.inspect_video(p)
                dur = meta.get("duration", 0.0)

                work_dir = settings.cache_dir / "shorts_work"
                work_dir.mkdir(parents=True, exist_ok=True)

                # Transcribe for timing boundaries
                wav_p = work_dir / f"{p.stem}_audio.wav"
                transcription_service.extract_audio(p, wav_p)
                trans = transcription_service.transcribe(wav_p)

                results = shorts_agent.produce_shorts(
                    video_path=p,
                    duration_sec=dur,
                    transcription=trans,
                    work_dir=work_dir,
                    max_shorts=1
                )

                if not results:
                    return "⚠️ Could not locate a segment meeting criteria.", None, None

                candidate, out_path = results[0]
                info_text = (
                    f"### 🎯 Rendered Short: `{candidate.title}`\n"
                    f"- **Duration**: **{candidate.duration_sec:.1f}s** (Strictly verified $\\le 60$s)\n"
                    f"- **Timestamp Range**: `{candidate.start_sec:.1f}s` to `{candidate.end_sec:.1f}s`\n"
                    f"- **Selection Rationale**: {candidate.selection_rationale}\n"
                    f"- **Output Dimensions**: `1080x1920` vertical"
                )

                return info_text, str(out_path), str(out_path)

            except Exception as e:
                return format_error_for_ui(e), None, None

        def handle_load_shorts_sample():
            from services.video_service import video_service
            sample_p = settings.cache_dir / "sample_educational_lecture.mp4"
            if not sample_p.exists():
                video_service.create_sample_demo_video(sample_p)
            return str(sample_p), "✅ Loaded educational lecture sample video for Shorts reframing."

        load_shorts_sample_btn.click(
            fn=handle_load_shorts_sample,
            inputs=[],
            outputs=[video_file, candidate_info_box]
        )

        generate_shorts_btn.click(
            fn=handle_shorts_extraction,
            inputs=[video_file, hook_override, cta_override],
            outputs=[candidate_info_box, short_video_player, download_short_file]
        )
