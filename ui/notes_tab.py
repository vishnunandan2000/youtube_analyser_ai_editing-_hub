"""
Automatic Handwritten Study Notes Tab.
"""

import gradio as gr
from pathlib import Path
from agents.notes_agent import notes_agent
from models.schemas import TranscriptionResult
from config import settings
from utils.error_handlers import format_error_for_ui

def create_notes_tab():
    with gr.Tab("Handwritten Study Notes", id="tab_notes"):
        gr.Markdown("## 📝 Automatic Handwritten Study & Revision Notes")
        gr.Markdown("Synthesizes complete educational lecture transcripts into formatted A4 PDF study notes with notebook margin ruling and instant page previews.")

        with gr.Row():
            with gr.Column(scale=1):
                notes_preset = gr.Dropdown(
                    label="⚡ Load Educational Topic Preset",
                    choices=[
                        "Generative AI & Attention Mechanisms",
                        "Cybersecurity Zero-Trust Architecture",
                        "Deep Learning Backpropagation & Math"
                    ],
                    value="Generative AI & Attention Mechanisms"
                )
                notes_title = gr.Textbox(label="Lecture / Subject Title", value="Generative AI: Comprehensive Architecture & Concepts")
                notes_author = gr.Textbox(label="Instructor / Curriculum Author", value="GenAI Studio Senior AI Architect")
                notes_transcript_input = gr.TextArea(
                    label="Lecture Speech Transcript (Editable)",
                    value="Generative Artificial Intelligence represents a significant evolution in machine learning. Unlike discriminative models that classify inputs, generative architectures predict or sample probability distributions to produce novel text, images, and audio. Transformers rely heavily on scaled dot-product attention: Attention(Q, K, V) = softmax(QK^T / sqrt(d_k))V. Key real-world applications include code synthesis, conversational RAG, and multimodal reasoning.",
                    lines=7
                )
                clean_print_toggle = gr.Checkbox(label="Clean Printable Monochrome Mode (disable notebook lines)", value=False)
                generate_notes_btn = gr.Button("📄 Generate Study Notes PDF", variant="primary", elem_classes=["action-btn-primary"])

            with gr.Column(scale=1):
                pdf_download = gr.File(label="Download Generated Notes (A4 PDF)")
                page_preview_gallery = gr.Gallery(label="Notes Page Previews (High Resolution)", columns=2, height=450)

        status_box = gr.Markdown("Ready to compile study notes.")

        def handle_notes_generation(title, transcript_text, clean_mode):
            if not transcript_text or not transcript_text.strip():
                return "⚠️ Please provide transcript text.", None, []
            try:
                out_pdf = settings.exports_dir / f"study_notes_{Path(title[:25]).stem}.pdf"
                dummy_trans = TranscriptionResult(text=transcript_text)
                pdf_path, page_images = notes_agent.create_notes_from_transcript(
                    video_title=title,
                    transcription=dummy_trans,
                    output_pdf_path=out_pdf,
                    clean_printable_mode=clean_mode
                )
                img_strs = [str(p) for p in page_images]
                return f"✅ Notes compiled successfully ({len(page_images)} pages rendered).", str(pdf_path), img_strs
            except Exception as e:
                return format_error_for_ui(e), None, []

        NOTE_PRESETS = {
            "Generative AI & Attention Mechanisms": (
                "Generative AI: Comprehensive Architecture & Concepts",
                "Generative Artificial Intelligence represents a significant evolution in machine learning. Unlike discriminative models that classify inputs, generative architectures predict or sample probability distributions to produce novel text, images, and audio. Transformers rely heavily on scaled dot-product attention: Attention(Q, K, V) = softmax(QK^T / sqrt(d_k))V. Key real-world applications include code synthesis, conversational RAG, and multimodal reasoning."
            ),
            "Cybersecurity Zero-Trust Architecture": (
                "Zero Trust Network Security & Threat Modeling",
                "Zero Trust fundamentally rejects the traditional perimeter security model, operating on the core doctrine: Never Trust, Always Verify. Every transaction, packet, and identity token must undergo continuous cryptographic validation. Crucial defensive primitives include micro-segmentation, ephemeral tokens, deep packet inspection, and behavioral anomaly detection across cloud infrastructure."
            ),
            "Deep Learning Backpropagation & Math": (
                "Deep Learning: Gradient Descent & Backpropagation Derivation",
                "Neural network optimization is governed by the chain rule of calculus. The loss function L computes deviation between predicted logits and target labels. Through reverse-mode automatic differentiation, gradients dL/dW are efficiently propagated backwards layer-by-layer: W := W - alpha * dL/dW, allowing deep parameter spaces to converge toward optimal representations."
            )
        }

        def handle_note_preset(choice):
            if choice in NOTE_PRESETS:
                t, txt = NOTE_PRESETS[choice]
                return t, txt
            return "Educational Synthesis", "Lecture transcription overview."

        notes_preset.change(
            fn=handle_note_preset,
            inputs=[notes_preset],
            outputs=[notes_title, notes_transcript_input]
        )

        generate_notes_btn.click(
            fn=handle_notes_generation,
            inputs=[notes_title, notes_transcript_input, clean_print_toggle],
            outputs=[status_box, pdf_download, page_preview_gallery]
        )
