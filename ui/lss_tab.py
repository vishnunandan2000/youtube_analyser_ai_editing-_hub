"""
Like, Share, Comment, and Subscribe Animation Studio Tab.
"""

import gradio as gr
from pathlib import Path
from services.animation_service import animation_service
from config import settings
from utils.error_handlers import format_error_for_ui

def create_lss_tab():
    with gr.Tab("Like, Share & Subscribe Animations", id="tab_lss"):
        gr.Markdown("## 🔔 Like, Share, Comment & Subscribe Animation Studio")
        gr.Markdown("Design and render original animated engagement lower-third overlays with custom channel branding, button click animations, and bell chimes.")

        with gr.Row():
            with gr.Column(scale=1):
                channel_name_input = gr.Textbox(label="Channel Name", value="AI Mastery Hub")
                subs_count_input = gr.Textbox(label="Subscriber Count Display", value="150K Subscribers")
                duration_slider = gr.Slider(label="Overlay Duration (seconds)", minimum=4.0, maximum=10.0, value=6.0, step=0.5)
                render_lss_btn = gr.Button("🔔 Render Engagement Animation", variant="primary", elem_classes=["action-btn-primary"])

            with gr.Column(scale=1):
                lss_preview_video = gr.Video(label="Rendered Lower-Third Animation Preview")
                download_lss_file = gr.File(label="Download Reusable MP4 Overlay")

        status_box = gr.Markdown("Ready to render engagement overlay.")

        def handle_lss_rendering(ch_name, subs, dur):
            try:
                work_dir = settings.cache_dir / "lss_work"
                work_dir.mkdir(parents=True, exist_ok=True)
                out_path = settings.exports_dir / f"engagement_overlay_{int(dur)}s.mp4"

                animation_service.create_like_share_subscribe_overlay(
                    channel_name=ch_name,
                    subscriber_count=subs,
                    duration_sec=float(dur),
                    output_video_path=out_path,
                    work_dir=work_dir
                )
                return f"✅ Engagement overlay rendered for '{ch_name}' ({dur:.1f}s)!", str(out_path), str(out_path)
            except Exception as e:
                return format_error_for_ui(e), None, None

        render_lss_btn.click(
            fn=handle_lss_rendering,
            inputs=[channel_name_input, subs_count_input, duration_slider],
            outputs=[status_box, lss_preview_video, download_lss_file]
        )
