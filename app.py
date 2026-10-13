"""
GenAI Video Intelligence Studio — Main Application Entrypoint.
Production-grade Gradio application unifying Division A (YouTube Intelligence)
and Division B (Autonomous Video Editing & Production).
"""

import gradio as gr
from config import settings
from ui.styles import STUDIO_CSS
from ui.dashboard import create_dashboard_tab
from ui.youtube_tab import create_youtube_tab
from ui.video_editor_tab import create_video_editor_tab
from ui.captions_tab import create_captions_tab
from ui.animation_tab import create_animation_tab
from ui.thumbnail_tab import create_thumbnail_tab
from ui.notes_tab import create_notes_tab
from ui.shorts_tab import create_shorts_tab
from ui.lss_tab import create_lss_tab
from ui.chatbot_tab import create_chatbot_tab
from ui.export_tab import create_export_tab
from ui.settings_tab import create_settings_tab
from utils.logging_config import logger

def get_studio_theme() -> gr.themes.Default:
    return gr.themes.Default(
        primary_hue="indigo",
        secondary_hue="pink",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "sans-serif"]
    ).set(
        # Base backgrounds
        body_background_fill="#0B0F19",
        body_background_fill_dark="#0B0F19",
        background_fill_primary="#131A2B",
        background_fill_primary_dark="#131A2B",
        background_fill_secondary="#0F172A",
        background_fill_secondary_dark="#0F172A",
        panel_background_fill="#131A2B",
        panel_background_fill_dark="#131A2B",
        panel_border_color="#1E293B",
        panel_border_color_dark="#1E293B",

        # Text colors
        body_text_color="#F8FAFC",
        body_text_color_dark="#F8FAFC",
        body_text_color_subdued="#94A3B8",
        body_text_color_subdued_dark="#94A3B8",

        # Blocks
        block_background_fill="#131A2B",
        block_background_fill_dark="#131A2B",
        block_border_color="#1E293B",
        block_border_color_dark="#1E293B",
        block_label_background_fill="#1E293B",
        block_label_background_fill_dark="#1E293B",
        block_label_text_color="#94A3B8",
        block_label_text_color_dark="#94A3B8",
        block_title_text_color="#F8FAFC",
        block_title_text_color_dark="#F8FAFC",

        # Inputs
        input_background_fill="#0F172A",
        input_background_fill_dark="#0F172A",
        input_background_fill_focus="#162036",
        input_background_fill_focus_dark="#162036",
        input_background_fill_hover="#131C30",
        input_background_fill_hover_dark="#131C30",
        input_border_color="#334155",
        input_border_color_dark="#334155",
        input_border_color_focus="#6366F1",
        input_border_color_focus_dark="#6366F1",
        input_border_color_hover="#475569",
        input_border_color_hover_dark="#475569",
        input_placeholder_color="#64748B",
        input_placeholder_color_dark="#64748B",

        # Primary Buttons
        button_primary_background_fill="#6366F1",
        button_primary_background_fill_dark="#6366F1",
        button_primary_background_fill_hover="#4F46E5",
        button_primary_background_fill_hover_dark="#4F46E5",
        button_primary_border_color="#6366F1",
        button_primary_border_color_dark="#6366F1",
        button_primary_text_color="#FFFFFF",
        button_primary_text_color_dark="#FFFFFF",
        button_primary_text_color_hover="#FFFFFF",
        button_primary_text_color_hover_dark="#FFFFFF",

        # Secondary Buttons
        button_secondary_background_fill="#1E293B",
        button_secondary_background_fill_dark="#1E293B",
        button_secondary_background_fill_hover="#334155",
        button_secondary_background_fill_hover_dark="#334155",
        button_secondary_border_color="#334155",
        button_secondary_border_color_dark="#334155",
        button_secondary_text_color="#F8FAFC",
        button_secondary_text_color_dark="#F8FAFC",
        button_secondary_text_color_hover="#FFFFFF",
        button_secondary_text_color_hover_dark="#FFFFFF",

        # Cancel / Neutral Buttons
        button_cancel_background_fill="#374151",
        button_cancel_background_fill_dark="#374151",
        button_cancel_background_fill_hover="#4B5563",
        button_cancel_background_fill_hover_dark="#4B5563",
        button_cancel_text_color="#F8FAFC",
        button_cancel_text_color_dark="#F8FAFC",

        # Checkboxes
        checkbox_background_color="#0F172A",
        checkbox_background_color_dark="#0F172A",
        checkbox_background_color_selected="#6366F1",
        checkbox_background_color_selected_dark="#6366F1",
        checkbox_background_color_focus="#6366F1",
        checkbox_background_color_focus_dark="#6366F1",
        checkbox_background_color_hover="#1E293B",
        checkbox_background_color_hover_dark="#1E293B",
        checkbox_border_color="#334155",
        checkbox_border_color_dark="#334155",
        checkbox_border_color_focus="#6366F1",
        checkbox_border_color_focus_dark="#6366F1",
        checkbox_border_color_hover="#6366F1",
        checkbox_border_color_hover_dark="#6366F1",
        checkbox_label_background_fill="#131A2B",
        checkbox_label_background_fill_dark="#131A2B",
        checkbox_label_background_fill_hover="#1E293B",
        checkbox_label_background_fill_hover_dark="#1E293B",
        checkbox_label_background_fill_selected="#1E293B",
        checkbox_label_background_fill_selected_dark="#1E293B",
        checkbox_label_text_color="#F8FAFC",
        checkbox_label_text_color_dark="#F8FAFC",
        checkbox_label_text_color_selected="#F8FAFC",
        checkbox_label_text_color_selected_dark="#F8FAFC",

        # Tables
        table_border_color="#1E293B",
        table_border_color_dark="#1E293B",
        table_even_background_fill="#131A2B",
        table_even_background_fill_dark="#131A2B",
        table_odd_background_fill="#0F172A",
        table_odd_background_fill_dark="#0F172A",
        table_row_focus="#1E293B",
        table_row_focus_dark="#1E293B",
        table_text_color="#F8FAFC",
        table_text_color_dark="#F8FAFC"
    )

theme = get_studio_theme()

def build_app() -> gr.Blocks:
    """Build the unified multi-tab Gradio Blocks interface."""
    with gr.Blocks(title="GenAI Video Intelligence Studio") as demo:
        # Header banner
        with gr.Row(elem_classes=["studio-header"]):
            with gr.Column(scale=8):
                gr.HTML("""
                <div style="display:flex; align-items:center; gap:16px;">
                    <div style="background:linear-gradient(135deg, #6366F1, #EC4899); border-radius:12px; width:48px; height:48px; display:flex; align-items:center; justify-content:center; font-size:24px;">
                        ⚡
                    </div>
                    <div>
                        <h1 style="margin:0; font-size:24px; font-weight:800; letter-spacing:-0.5px; color:#FFFFFF;">
                            GenAI Video Intelligence Studio
                        </h1>
                        <p style="margin:3px 0 0 0; color:#94A3B8; font-size:13px;">
                            Autonomous Video Analytics, Intelligent Multilingual Production & Educational Motion Graphics
                        </p>
                    </div>
                </div>
                """)
            with gr.Column(scale=4, elem_classes=["header-badges"]):
                gr.HTML("""
                <div style="display:flex; justify-content:flex-end; gap:8px; align-items:center; height:100%;">
                    <span class="division-badge-a">DIVISION A • YOUTUBE INTEL</span>
                    <span class="division-badge-b">DIVISION B • PRODUCTION STUDIO</span>
                </div>
                """)

        # 12 Navigation Tabs
        with gr.Tabs(elem_id="studio_tabs"):
            create_dashboard_tab()
            create_youtube_tab()
            create_video_editor_tab()
            create_captions_tab()
            create_animation_tab()
            create_thumbnail_tab()
            create_notes_tab()
            create_shorts_tab()
            create_lss_tab()
            create_chatbot_tab()
            create_export_tab()
            create_settings_tab()

        # Footer
        gr.HTML("""
        <div style="text-align:center; padding:24px; color:#64748B; font-size:12px; border-top:1px solid #1E293B; margin-top:32px;">
            GenAI Video Intelligence Studio • Engineered with Gradio 6, local Llama 3.2 (Ollama), FFmpeg & faster-whisper.
        </div>
        """)

        # Enforce dark mode class on DOM root immediately upon mount
        demo.load(
            None,
            None,
            None,
            js="() => { document.documentElement.classList.add('dark'); document.body.classList.add('dark'); const c = document.querySelector('.gradio-container'); if (c) c.classList.add('dark'); }"
        )

    return demo

app = build_app()

if __name__ == "__main__":
    logger.info("Starting GenAI Video Intelligence Studio server...")
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        theme=theme,
        css=STUDIO_CSS,
        show_error=True
    )
