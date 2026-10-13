"""
Overview Dashboard Tab.
Presents the executive summary of the studio, active divisions, and quick action launchpads.
"""

import gradio as gr
from services.ollama_service import ollama_service
from services.storage_service import storage_service

def create_dashboard_tab():
    with gr.Tab("Overview Dashboard", id="tab_overview"):
        gr.Markdown("""
        # 🚀 GenAI Video Intelligence Studio
        ### Unified Multi-Agent Platform for Video Analytics & Autonomous Educational Production
        """)

        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML("""
                <div style="background:#131A2B; border:1px solid #3B82F6; border-radius:12px; padding:20px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="background:#3B82F6; color:white; font-size:10px; font-weight:700; padding:3px 8px; border-radius:12px;">DIVISION A</span>
                        <span style="color:#60A5FA; font-size:20px;">📊</span>
                    </div>
                    <h3 style="color:#F8FAFC; margin-top:12px; margin-bottom:6px;">YouTube Intelligence</h3>
                    <p style="color:#94A3B8; font-size:13px; line-height:1.4;">
                        High-precision YouTube URL metrics, public & authorized analytics, Llama 3.2 comment sentiment classification (Positive/Negative/Neutral), topic clustering, and creative Copilot.
                    </p>
                </div>
                """)

            with gr.Column(scale=1):
                gr.HTML("""
                <div style="background:#131A2B; border:1px solid #EC4899; border-radius:12px; padding:20px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="background:#EC4899; color:white; font-size:10px; font-weight:700; padding:3px 8px; border-radius:12px;">DIVISION B</span>
                        <span style="color:#F472B6; font-size:20px;">🎬</span>
                    </div>
                    <h3 style="color:#F8FAFC; margin-top:12px; margin-bottom:6px;">Autonomous Video Production</h3>
                    <p style="color:#94A3B8; font-size:13px; line-height:1.4;">
                        Upload long lectures, synthesize structured Edit Decision Lists (EDL), auto-cut pauses, generate subtitles & dubbing across 12 languages, render educational animations, study notes PDF, and vertical Shorts (≤60s).
                    </p>
                </div>
                """)

            with gr.Column(scale=1):
                health = ollama_service.check_health()
                status_color = "#10B981" if health["model_ready"] else "#EF4444"
                status_text = "READY" if health["model_ready"] else "ATTENTION NEEDED"
                gr.HTML(f"""
                <div style="background:#131A2B; border:1px solid #10B981; border-radius:12px; padding:20px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="background:{status_color}; color:white; font-size:10px; font-weight:700; padding:3px 8px; border-radius:12px;">SYSTEM STATUS</span>
                        <span style="color:#34D399; font-size:20px;">⚡</span>
                    </div>
                    <h3 style="color:#F8FAFC; margin-top:12px; margin-bottom:6px;">Llama 3.2: {status_text}</h3>
                    <p style="color:#94A3B8; font-size:13px; line-height:1.4;">
                        Ollama: <b>{health['base_url']}</b><br/>
                        Model: <b>{health['configured_model']}</b><br/>
                        FFmpeg: <b>Active & Ready</b>
                    </p>
                </div>
                """)

        gr.Markdown("---")
        gr.Markdown("### 🌟 Feature Navigation Quick Guide")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("""
                - **YouTube Intelligence**: Enter any video URL to inspect reach, like/comment ratios, and comment sentiments.
                - **Automatic Video Editor**: Upload lecture files, auto-detect scene cuts, remove dead pauses, and export edited MP4.
                - **Multilingual Captions & Dubbing**: Subtitles & neural voice synthesis across 12 languages (Hindi, Spanish, Telugu, etc.).
                - **Animation Studio**: Create procedural motion graphics (ML flow, Neural Net, Firewall) based on reference principles.
                """)
            with gr.Column():
                gr.Markdown(r"""
                - **AI Thumbnail Generator**: Render 3 distinctive 1280x720 thumbnail concepts with instructor logo support.
                - **Handwritten Study Notes**: Convert speech transcripts into formatted A4 study PDFs with notebook styling.
                - **YouTube Shorts Generator**: Automatically reframe to 9:16 vertical video with kinetic captions (strictly $\le 60$s).
                - **AI Copilot & Diagnostics**: Chat with Llama 3.2 for hooks, titles, chapters, and verify system dependencies.
                """)
