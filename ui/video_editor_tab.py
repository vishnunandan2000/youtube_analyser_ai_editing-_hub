"""
Division B — Autonomous Video Editor Tab.
Upload video lectures, configure production parameters, execute autonomous multi-agent editing pipeline.
"""

import gradio as gr
from pathlib import Path
from agents.orchestrator import orchestrator
from utils.error_handlers import format_error_for_ui
from services.translation_service import SUPPORTED_LANGUAGES

def create_video_editor_tab():
    with gr.Tab("Automatic Video Editor", id="tab_video_editor"):
        gr.HTML("""
        <div style="margin-bottom:16px;">
            <span class="division-badge-b">DIVISION B</span>
            <h2 style="display:inline-block; margin-left:12px; margin-top:0; color:#F8FAFC;">Autonomous Video Production Studio</h2>
        </div>
        """)

        with gr.Row():
            with gr.Column(scale=1):
                video_input = gr.Video(label="Upload Raw Video Lecture / Demo", sources=["upload"])
                with gr.Row():
                    load_sample_btn = gr.Button("🎬 Load Sample Educational Video", variant="secondary", size="sm")
                trainer_img = gr.Image(label="Optional Trainer Photo / Channel Logo", type="filepath")

            with gr.Column(scale=1):
                with gr.Accordion("⚙️ Video Pipeline Settings", open=True):
                    with gr.Row():
                        source_lang = gr.Dropdown(
                            label="Source Audio Language",
                            choices=["auto (Auto-detect)"] + [f"{code} ({name})" for code, name in SUPPORTED_LANGUAGES.items()],
                            value="auto (Auto-detect)"
                        )
                        target_lang = gr.Dropdown(
                            label="Target Audio & Caption Language",
                            choices=[(f"{name} ({code})", code) for code, name in SUPPORTED_LANGUAGES.items()],
                            value="en"
                        )

                    with gr.Row():
                        output_res = gr.Dropdown(
                            label="Output Resolution",
                            choices=["1080p (1920x1080 Full HD)", "720p (1280x720 HD)", "480p (854x480 SD)"],
                            value="720p (1280x720 HD)"
                        )
                        output_fps = gr.Dropdown(
                            label="Output Frame Rate",
                            choices=["24 fps (Cinematic)", "30 fps (Standard)", "60 fps (Smooth)"],
                            value="30 fps (Standard)"
                        )

                    with gr.Row():
                        edit_style = gr.Dropdown(
                            label="Editing Style",
                            choices=["Educational Gentle (Preserve all formulas & code)", "Standard Fast Cut", "Snappy Micro-Lecture"],
                            value="Educational Gentle (Preserve all formulas & code)"
                        )
                        sub_style = gr.Dropdown(
                            label="Subtitle Style",
                            choices=["Classic White with Shadow", "Vibrant Yellow / Neon Box", "Minimalist Lower-Third Banner"],
                            value="Classic White with Shadow"
                        )

                    with gr.Row():
                        anim_intensity = gr.Dropdown(
                            label="Animation Intensity",
                            choices=["Subtle (Key moments only)", "Standard (Every topic transition)", "Dynamic (High-energy visuals)"],
                            value="Standard (Every topic transition)"
                        )
                        export_fmt = gr.Dropdown(
                            label="Export Container Format",
                            choices=["MP4 (H.264 / AAC - Recommended)", "MKV", "MOV"],
                            value="MP4 (H.264 / AAC - Recommended)"
                        )

                    with gr.Row():
                        bg_music_toggle = gr.Checkbox(label="Add Ambient Lo-Fi Background Music", value=False)
                        burn_captions = gr.Checkbox(label="Burn Synchronized Captions into Video", value=True)
                        anim_toggle = gr.Checkbox(label="Generate Motion Graphics & Overlays", value=True)

                    with gr.Row():
                        orig_vol_slider = gr.Slider(label="Original Audio Volume", minimum=0.0, maximum=1.0, value=0.2, step=0.05)
                        dub_vol_slider = gr.Slider(label="Dubbed / Narration Volume", minimum=0.0, maximum=1.0, value=1.0, step=0.05)

                    with gr.Row():
                        shorts_toggle = gr.Checkbox(label="Generate YouTube Shorts (≤60s)", value=True)
                        notes_toggle = gr.Checkbox(label="Generate Handwritten Study Notes PDF", value=True)
                        thumbs_toggle = gr.Checkbox(label="Generate AI Thumbnail Concepts", value=True)

                    channel_brand = gr.Textbox(label="Channel Brand Name", value="AI Mastery Academy")

                run_pipeline_btn = gr.Button("⚡ Run Autonomous Editing Pipeline", variant="primary", elem_classes=["action-btn-primary"])

        pipeline_status = gr.Markdown("Ready to process. Upload a video file or click 'Load Sample Educational Video'.")

        gr.Markdown("---")
        gr.Markdown("### 🎥 Rendered Video & Master Output Preview")

        with gr.Row():
            with gr.Column(scale=1):
                edited_preview = gr.Video(label="Rendered Edited Video Preview")
            with gr.Column(scale=1):
                job_report_md = gr.Markdown("Pipeline stage details and EDL records will appear here upon completion.")

        # Sample video loader handler
        def handle_load_sample():
            from services.video_service import video_service
            from config import settings
            sample_p = settings.cache_dir / "sample_educational_lecture.mp4"
            if not sample_p.exists():
                video_service.create_sample_demo_video(sample_p)
            return str(sample_p), "✅ Loaded synthetic educational lecture sample video (12s with formulas and slide visuals)."

        load_sample_btn.click(
            fn=handle_load_sample,
            inputs=[],
            outputs=[video_input, pipeline_status]
        )

        # Execution handler
        def handle_production_pipeline(
            v_file, t_img, s_lang, t_lang, out_res, out_fps, e_style, s_style,
            a_intensity, exp_fmt, bg_music, b_captions, g_anim, orig_vol, dub_vol,
            g_shorts, g_notes, g_thumbs, ch_name
        ):
            if not v_file:
                return "⚠️ Please upload a video file or click 'Load Sample Educational Video'.", None, "No video provided."

            try:
                res = orchestrator.run_full_production_pipeline(
                    video_input_path=v_file,
                    trainer_image_path=t_img,
                    source_language=s_lang,
                    target_language=t_lang,
                    output_resolution=out_res,
                    output_fps=out_fps,
                    edit_style=e_style,
                    subtitle_style=s_style,
                    animation_intensity=a_intensity,
                    export_format=exp_fmt,
                    bg_music=bool(bg_music),
                    original_volume=float(orig_vol),
                    dubbed_volume=float(dub_vol),
                    generate_shorts=bool(g_shorts),
                    generate_thumbnails=bool(g_thumbs),
                    generate_notes=bool(g_notes),
                    generate_animations=bool(g_anim),
                    burn_captions=bool(b_captions),
                    custom_channel_name=ch_name
                )
                job = res["job"]
                report = f"### 🎉 Pipeline Job Complete: `{job.job_id}`\n\n"
                report += f"- **Status**: `{job.status.value}`\n"
                report += f"- **Resolution / FPS**: `{out_res}` @ `{out_fps}`\n"
                report += f"- **Edit & Subtitle Style**: `{e_style}` • `{s_style}`\n"
                report += f"- **Artifacts Produced**: {len(job.artifacts)}\n\n"
                report += "#### 📦 Generated Assets in Export Center:\n"
                for art in job.artifacts:
                    report += f"- **{art.name}** ({art.category}) — `{Path(art.file_path).name}` ({art.file_size_bytes / 1024:.1f} KB)\n"

                # Find primary video output
                video_out = next((art.file_path for art in job.artifacts if art.category == "Video"), None)

                return "✅ Pipeline finished successfully! All assets ready.", video_out, report

            except Exception as e:
                err = format_error_for_ui(e)
                return err, None, f"**Pipeline Error**: {str(e)}"

        run_pipeline_btn.click(
            fn=handle_production_pipeline,
            inputs=[
                video_input, trainer_img, source_lang, target_lang, output_res, output_fps,
                edit_style, sub_style, anim_intensity, export_fmt, bg_music_toggle,
                burn_captions, anim_toggle, orig_vol_slider, dub_vol_slider,
                shorts_toggle, notes_toggle, thumbs_toggle, channel_brand
            ],
            outputs=[pipeline_status, edited_preview, job_report_md]
        )

