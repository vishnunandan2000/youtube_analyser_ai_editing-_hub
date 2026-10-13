"""
AI Video Content Improvement Chatbot & Copilot Tab.
"""

import gradio as gr
from typing import List, Dict, Any
from agents.content_strategy_agent import content_strategy_agent
from services.ollama_service import ollama_service
from utils.error_handlers import format_error_for_ui

def create_chatbot_tab():
    with gr.Tab("AI Content Improvement Chatbot", id="tab_chatbot"):
        gr.Markdown("## 🤖 AI Video Content Copilot & Creative Strategist")
        gr.Markdown("Powered by local Ollama (`llama3.2:latest`). Analyzes actual video metrics, transcripts, and audience sentiment to generate targeted recommendations.")

        with gr.Row():
            with gr.Column(scale=2):
                chatbot_ui = gr.Chatbot(
                    label="Conversational Creative Assistant",
                    height=450
                )
                with gr.Row():
                    user_msg = gr.Textbox(
                        label="Message Copilot",
                        placeholder="Ask how to improve the opening hook, fix pacing, or explain a complex formula...",
                        lines=1,
                        scale=4
                    )
                    send_btn = gr.Button("Send", variant="primary", scale=1, elem_classes=["action-btn-primary"])

            with gr.Column(scale=1):
                gr.Markdown("### ⚡ Quick Strategy Actions")
                btn_titles = gr.Button("💡 Suggest Better Titles", variant="secondary")
                btn_hooks = gr.Button("🪝 Generate Stronger Opening Hooks", variant="secondary")
                btn_thumbs = gr.Button("🎨 Suggest Thumbnail Concepts", variant="secondary")
                btn_chapters = gr.Button("📑 Generate Video Chapter Plan", variant="secondary")
                btn_plan = gr.Button("📊 Generate Comprehensive Improvement Plan", variant="secondary")
                btn_export = gr.Button("📥 Export Recommendations", variant="primary", elem_classes=["action-btn-primary"])
                export_recommendations_file = gr.File(label="Download Recommendations JSON/MD", visible=True)

                with gr.Accordion("📌 Active Context Parameters", open=True):
                    context_title = gr.Textbox(label="Active Video Title", value="Generative AI Explained In 5 Minutes")
                    context_topics = gr.Textbox(label="Key Topics", value="Foundation Models, LLMs, Attention Mechanism, RAG")

        # Chat response handler
        def respond_chat(message, history, title, topics):
            if not message or not message.strip():
                return history, ""

            # Convert gradio chat history to standard format
            hist_formatted = []
            for h in (history or []):
                # Handle both tuple format and dict format
                if isinstance(h, (list, tuple)) and len(h) == 2:
                    hist_formatted.append({"role": "user", "content": str(h[0])})
                    hist_formatted.append({"role": "assistant", "content": str(h[1])})
                elif isinstance(h, dict):
                    hist_formatted.append(h)

            context = {
                "title": title,
                "duration": 302,
                "topics": topics,
                "sentiment": "85% Positive, requests for code examples"
            }

            try:
                reply = content_strategy_agent.chat_response(message, hist_formatted, context)
            except Exception as e:
                reply = format_error_for_ui(e)

            new_history = list(history or [])
            new_history.append({"role": "user", "content": message})
            new_history.append({"role": "assistant", "content": reply})
            return new_history, ""

        send_btn.click(
            fn=respond_chat,
            inputs=[user_msg, chatbot_ui, context_title, context_topics],
            outputs=[chatbot_ui, user_msg]
        )
        user_msg.submit(
            fn=respond_chat,
            inputs=[user_msg, chatbot_ui, context_title, context_topics],
            outputs=[chatbot_ui, user_msg]
        )

        # Quick action button triggers
        def trigger_quick_action(action_type, history, title, topics):
            prompt_map = {
                "titles": "Please generate 5 high-converting, curiosity-driven YouTube titles for this video with brief rationales.",
                "hooks": "Please craft 3 high-retention 15-second opening hook scripts that prevent viewer drop-off in the first 30 seconds.",
                "thumbs": "Suggest 3 visual thumbnail scene concepts with specific layout instructions, text headlines, and color palettes.",
                "chapters": "Generate a clear, professional video chapter breakdown with timestamps and pedagogical segment titles.",
                "plan": "Generate an end-to-end video improvement plan addressing title, hook, pacing, animation insertion points, and engagement calls to action."
            }
            msg = prompt_map.get(action_type, "Help improve this video.")
            return respond_chat(msg, history, title, topics)

        btn_titles.click(
            fn=lambda h, t, tp: trigger_quick_action("titles", h, t, tp),
            inputs=[chatbot_ui, context_title, context_topics],
            outputs=[chatbot_ui, user_msg]
        )
        btn_hooks.click(
            fn=lambda h, t, tp: trigger_quick_action("hooks", h, t, tp),
            inputs=[chatbot_ui, context_title, context_topics],
            outputs=[chatbot_ui, user_msg]
        )
        btn_thumbs.click(
            fn=lambda h, t, tp: trigger_quick_action("thumbs", h, t, tp),
            inputs=[chatbot_ui, context_title, context_topics],
            outputs=[chatbot_ui, user_msg]
        )
        btn_chapters.click(
            fn=lambda h, t, tp: trigger_quick_action("chapters", h, t, tp),
            inputs=[chatbot_ui, context_title, context_topics],
            outputs=[chatbot_ui, user_msg]
        )
        btn_plan.click(
            fn=lambda h, t, tp: trigger_quick_action("plan", h, t, tp),
            inputs=[chatbot_ui, context_title, context_topics],
            outputs=[chatbot_ui, user_msg]
        )

        def handle_export_recommendations(history, title, topics):
            from pathlib import Path
            import json
            from config import settings
            safe_name = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).rstrip()
            out_path = settings.exports_dir / f"recommendations_{safe_name[:25]}.md"
            lines = [
                f"# AI Creative Improvement Report: {title}",
                f"**Focus Topics**: {topics}\n",
                "## Conversation Dialogue & Recommendations:\n"
            ]
            for turn in (history or []):
                if isinstance(turn, dict):
                    role = turn.get("role", "user").capitalize()
                    content = turn.get("content", "")
                elif isinstance(turn, (list, tuple)) and len(turn) == 2:
                    lines.append(f"### Creator\n{turn[0]}\n")
                    lines.append(f"### AI Copilot\n{turn[1]}\n")
                    continue
                else:
                    role, content = "Note", str(turn)
                lines.append(f"### {role}\n{content}\n")
            
            out_path.write_text("\n".join(lines), encoding="utf-8")
            return str(out_path)

        btn_export.click(
            fn=handle_export_recommendations,
            inputs=[chatbot_ui, context_title, context_topics],
            outputs=[export_recommendations_file]
        )
