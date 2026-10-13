"""
Settings and System Diagnostics Tab.
"""

import gradio as gr
import sys
import shutil
from pathlib import Path
from config import settings
from services.ollama_service import ollama_service
from services.oauth_service import oauth_service
from utils.media_utils import get_ffmpeg_path, get_ffprobe_path

def create_settings_tab():
    with gr.Tab("Settings & System Diagnostics", id="tab_settings"):
        gr.Markdown("## ⚙️ System Settings & Environment Diagnostics")
        gr.Markdown("Inspect active AI model connections, external media binaries, and configuration parameters.")

        with gr.Row():
            run_diag_btn = gr.Button("🔍 Run Full Diagnostics Check", variant="primary", elem_classes=["action-btn-primary"])

        diag_output_md = gr.Markdown("Click the button above to run diagnostic checks.")

        with gr.Accordion("🔧 Runtime Configuration Parameters", open=True):
            with gr.Row():
                cfg_ollama_url = gr.Textbox(label="Ollama Base URL", value=settings.ollama_base_url, interactive=False)
                cfg_ollama_model = gr.Textbox(label="Configured LLM Model", value=settings.ollama_model, interactive=False)
                cfg_timeout = gr.Number(label="Ollama Timeout (seconds)", value=settings.ollama_timeout_seconds, interactive=False)

            with gr.Row():
                cfg_db_url = gr.Textbox(label="Database URL", value=settings.database_url, interactive=False)
                cfg_max_upload = gr.Number(label="Max Upload Size (MB)", value=settings.max_upload_size_mb, interactive=False)
                cfg_max_dur = gr.Number(label="Max Duration (Minutes)", value=settings.max_video_duration_minutes, interactive=False)

        def run_diagnostics():
            health = ollama_service.check_health()
            auth_info = oauth_service.get_auth_status()
            ffmpeg_p = get_ffmpeg_path()
            ffprobe_p = get_ffprobe_path()

            # Format markdown report
            report = "### 📋 System Health Diagnostic Report\n\n"
            
            # Python
            report += f"- **Python Runtime**: `Python {sys.version.split()[0]}` on `{sys.platform}`\n"
            
            # Ollama
            ollama_icon = "✅" if health["model_ready"] else "⚠️"
            report += f"- **Ollama Connection**: {ollama_icon} `{health['status']}` at `{health['base_url']}`\n"
            report += f"  - *Model Status*: **{health['configured_model']}** {'(Available)' if health['model_ready'] else '(Not Found)'}\n"
            if health.get("available_models"):
                report += f"  - *Installed Local Models*: `{', '.join(health['available_models'])}`\n"
            if not health["model_ready"]:
                report += f"  - *Remediation*: Run `ollama run {settings.ollama_model}` in terminal.\n"

            # FFmpeg
            ffmpeg_icon = "✅" if ffmpeg_p else "❌"
            report += f"- **FFmpeg Binary**: {ffmpeg_icon} `{ffmpeg_p or 'Not Found in PATH or static_ffmpeg'}`\n"
            ffprobe_icon = "✅" if ffprobe_p else "❌"
            report += f"- **FFprobe Binary**: {ffprobe_icon} `{ffprobe_p or 'Not Found'}`\n"

            # YouTube API
            yt_api_configured = bool(settings.youtube_api_key)
            report += f"- **YouTube Data API v3**: {'✅ Configured' if yt_api_configured else 'ℹ️ Optional (yt-dlp public extractor active as fallback)'}\n"
            report += f"- **YouTube Analytics OAuth**: {auth_info['message']}\n"

            # Directory Storage
            report += f"- **Working Directory**: `{settings.base_dir}`\n"
            report += f"- **Exports Directory**: `{settings.exports_dir}` (Exists: {settings.exports_dir.exists()})\n"
            report += f"- **Jobs Cache Directory**: `{settings.jobs_dir}` (Exists: {settings.jobs_dir.exists()})\n"

            return report

        run_diag_btn.click(
            fn=run_diagnostics,
            inputs=[],
            outputs=[diag_output_md]
        )
