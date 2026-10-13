"""
Context-Aware Educational Animation Studio Tab.
"""

import gradio as gr
from pathlib import Path
from services.animation_service import animation_service
from config import settings
from utils.error_handlers import format_error_for_ui

def create_animation_tab():
    with gr.Tab("Animation Studio", id="tab_animation"):
        gr.Markdown("## 🎨 Context-Aware Educational Motion Graphics Studio")
        gr.Markdown("Render procedural 2D educational motion graphics and diagrams inspired by the Simplilearn reference explainer.")

        with gr.Row():
            with gr.Column(scale=1):
                preset_picker = gr.Dropdown(
                    label="⚡ Load Educational Concept Preset",
                    choices=[
                        "Machine Learning Training Pipeline",
                        "Deep Learning Neural Network",
                        "Cybersecurity Packet Filtering",
                        "Blockchain Distributed Ledger",
                        "Python Attention Algorithm Trace",
                        "Attention Scaled Dot-Product Math Derivation",
                        "Foundational Architecture Card"
                    ],
                    value="Machine Learning Training Pipeline"
                )
                concept_input = gr.Textbox(label="Educational Concept Title", value="Generative AI Foundation Models")
                anim_type = gr.Dropdown(
                    label="Animation Architecture Pattern",
                    choices=[
                        ("Machine Learning Pipeline Flow", "ML_PIPELINE"),
                        ("Deep Learning Neural Network", "NEURAL_NET"),
                        ("Cybersecurity Packet Inspection", "CYBER_PACKET"),
                        ("Blockchain Distributed Ledger", "BLOCKCHAIN_LEDGER"),
                        ("Programming Syntax & Algorithm Trace", "CODE_ALGORITHM"),
                        ("Mathematics & Derivation Formula Card", "MATHEMATICS_FORMULA"),
                        ("General Educational Highlight Card", "CONCEPT_CARD")
                    ],
                    value="ML_PIPELINE"
                )
                labels_input = gr.Textbox(
                    label="Stage Labels / Code Lines / Derivation Steps",
                    value="Data Ingestion, Tokenization, Foundation Model, Fine-Tuning, API Inference",
                    lines=3
                )
                duration_slider = gr.Slider(label="Duration (seconds)", minimum=3.0, maximum=12.0, value=5.0, step=1.0)
                render_anim_btn = gr.Button("🎬 Render Educational Animation", variant="primary", elem_classes=["action-btn-primary"])

            with gr.Column(scale=1):
                anim_video_preview = gr.Video(label="Rendered Motion Graphic Preview")
                download_anim_file = gr.File(label="Download MP4 Animation Clip")

        status_msg = gr.Markdown("Ready to render animations.")

        def handle_render_animation(concept, atype, labels_str, dur):
            try:
                lbls = [l.strip() for l in labels_str.split(",") if l.strip()]
                out_path = settings.exports_dir / f"anim_{atype.lower()}_{int(dur)}s.mp4"
                work_dir = settings.cache_dir / "anim_work"
                work_dir.mkdir(parents=True, exist_ok=True)

                animation_service.create_educational_animation(
                    concept=concept,
                    animation_type=atype,
                    labels=lbls,
                    duration_sec=float(dur),
                    output_video_path=out_path,
                    work_dir=work_dir
                )
                return f"✅ Animation '{concept}' rendered successfully!", str(out_path), str(out_path)
            except Exception as e:
                return format_error_for_ui(e), None, None

        PRESETS = {
            "Machine Learning Training Pipeline": (
                "ML Pipeline: Ingestion to Inference",
                "ML_PIPELINE",
                "Data Ingestion, Tokenization, Foundation Model, Fine-Tuning, API Inference"
            ),
            "Deep Learning Neural Network": (
                "Deep Neural Network & Attention Heads",
                "NEURAL_NET",
                "Input Tokens, Dense Projections, Multi-Head Attention, Output Logits"
            ),
            "Cybersecurity Packet Filtering": (
                "Zero Trust Network Inspection & Firewall",
                "CYBER_PACKET",
                "Encrypted Traffic, Stateful Inspection, Deep Packet Analysis, Secure Verification"
            ),
            "Blockchain Distributed Ledger": (
                "Decentralized Ledger Consensus",
                "BLOCKCHAIN_LEDGER",
                "Block #101 (Genesis), Block #102 (Txs Verified), Block #103 (Consensus)"
            ),
            "Python Attention Algorithm Trace": (
                "Scaled Dot-Product Attention Implementation",
                "CODE_ALGORITHM",
                "def forward_attention(Q, K, V):,    scores = matmul(Q, K.T) / sqrt(d_k),    weights = softmax(scores),    return matmul(weights, V)"
            ),
            "Attention Scaled Dot-Product Math Derivation": (
                "Mathematical Proof of Attention Scaling",
                "MATHEMATICS_FORMULA",
                "1. Given input embeddings X in R^(N x d), 2. Compute Q=XW_Q and K=XW_K, 3. Normalize: S = QK^T / sqrt(d_k), 4. Distribution: P = softmax(S), 5. Output = P * V"
            ),
            "Foundational Architecture Card": (
                "Core Transformers Architecture Overview",
                "CONCEPT_CARD",
                "Self-Attention mechanism, Positional Encodings, Residual Connections, Layer Normalization"
            )
        }

        def handle_preset_change(choice):
            if choice in PRESETS:
                c, t, l = PRESETS[choice]
                return c, t, l
            return "Generative AI Concept", "ML_PIPELINE", "Input, Process, Output"

        preset_picker.change(
            fn=handle_preset_change,
            inputs=[preset_picker],
            outputs=[concept_input, anim_type, labels_input]
        )

        render_anim_btn.click(
            fn=handle_render_animation,
            inputs=[concept_input, anim_type, labels_input, duration_slider],
            outputs=[status_msg, anim_video_preview, download_anim_file]
        )

