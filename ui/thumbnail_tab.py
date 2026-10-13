"""
AI Thumbnail Generator Tab.
"""

import gradio as gr
from pathlib import Path
from services.thumbnail_service import thumbnail_service
from config import settings
from utils.error_handlers import format_error_for_ui

def create_thumbnail_tab():
    with gr.Tab("AI Thumbnail Generator", id="tab_thumbnail"):
        gr.Markdown("## 🖼️ AI YouTube Thumbnail Generator (1280 × 720)")
        gr.Markdown("Render 3 distinct thumbnail concepts locally using Pillow with custom instructor photo / logo compositing.")

        with gr.Row():
            with gr.Column(scale=1):
                thumb_title = gr.Textbox(label="Main Headline", value="GENERATIVE AI EXPLAINED IN 5 MINUTES")
                thumb_subtitle = gr.Textbox(label="Subtitle / Hook", value="THE COMPLETE PRACTICAL BLUEPRINT")
                thumb_badge = gr.Textbox(label="Category Badge", value="AI MASTERCLASS")
                trainer_photo = gr.Image(label="Optional Trainer Photo or Logo (PNG with transparent bg recommended)", type="filepath")
                generate_thumbs_btn = gr.Button("✨ Generate 3 Thumbnail Concepts", variant="primary", elem_classes=["action-btn-primary"])

            with gr.Column(scale=2):
                with gr.Row():
                    concept_1_img = gr.Image(label="Concept 1: High-Impact Cyber Tech", height=240)
                    concept_2_img = gr.Image(label="Concept 2: Minimalist Executive Modern", height=240)
                with gr.Row():
                    concept_3_img = gr.Image(label="Concept 3: High-Energy Explainer", height=240)
                    download_thumbs = gr.File(label="Download High-Res Concepts")

        status_box = gr.Markdown("Ready to generate thumbnails.")

        def handle_thumbnails(title, subtitle, badge, photo):
            if not title or not title.strip():
                return "⚠️ Please enter a title.", None, None, None, None
            try:
                out_dir = settings.exports_dir / "thumbnails"
                out_dir.mkdir(parents=True, exist_ok=True)
                p_photo = Path(photo) if photo else None
                concepts = thumbnail_service.generate_concepts(
                    title=title,
                    subtitle=subtitle,
                    badge_text=badge,
                    trainer_image_path=p_photo,
                    output_dir=out_dir
                )
                return (
                    f"✅ Successfully generated {len(concepts)} thumbnail concepts at 1280x720!",
                    str(concepts[0]),
                    str(concepts[1]),
                    str(concepts[2]),
                    [str(c) for c in concepts]
                )
            except Exception as e:
                return format_error_for_ui(e), None, None, None, None

        generate_thumbs_btn.click(
            fn=handle_thumbnails,
            inputs=[thumb_title, thumb_subtitle, thumb_badge, trainer_photo],
            outputs=[status_box, concept_1_img, concept_2_img, concept_3_img, download_thumbs]
        )
