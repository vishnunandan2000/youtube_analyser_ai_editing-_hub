"""
Content Strategy Agent and Interactive AI Video Copilot.
Generates structured video improvement plans, catchy titles, opening hooks,
thumbnail concepts, and chapter plans powered by Llama 3.2.
"""

from typing import Dict, Any, List, Optional
import json
from models.analytics_models import VideoImprovementReport, VideoImprovementItem, RecommendationPriority
from services.ollama_service import ollama_service
from utils.logging_config import logger

class ContentStrategyAgent:
    def __init__(self):
        pass

    def generate_comprehensive_improvement_plan(
        self,
        video_title: str,
        video_duration: float,
        kpis_summary: str,
        sentiment_summary: str,
        audience_feedback_text: str
    ) -> VideoImprovementReport:
        """
        Generate a multi-faceted improvement plan based strictly on the analyzed data.
        """
        system_prompt = (
            "You are a principal video content strategist and educational media director.\n"
            "Analyze the video's actual metrics, sentiment breakdown, and audience feedback.\n"
            "Generate an exhaustive, realistic improvement report formatted as a JSON object with keys:\n"
            "- 'suggested_titles': list of 5 high-converting, curiosity-driven YouTube titles\n"
            "- 'opening_hooks': list of 3 high-retention 15-second opening hook scripts\n"
            "- 'thumbnail_concepts': list of 3 visual thumbnail scene concepts\n"
            "- 'chapter_plan': list of objects with 'timestamp_approx' and 'chapter_title'\n"
            "- 'recommendations': list of objects with:\n"
            "    * 'category': ('Hook' | 'Pacing' | 'Thumbnail' | 'Explanation' | 'CallToAction')\n"
            "    * 'priority': ('Critical' | 'High' | 'Medium' | 'Low')\n"
            "    * 'observed_problem': specific issue noted in data or common video weaknesses\n"
            "    * 'supporting_evidence': reference to audience feedback or retention principles\n"
            "    * 'proposed_improvement': concrete creative change\n"
            "    * 'expected_benefit': realistic pedagogical or engagement gain (do not promise guaranteed viral numbers)\n"
            "    * 'implementation_steps': array of 2-3 practical steps\n"
            "Return valid JSON only."
        )

        user_prompt = (
            f"Video Title: {video_title}\n"
            f"Duration: {video_duration} seconds\n"
            f"KPIs: {kpis_summary}\n"
            f"Sentiment: {sentiment_summary}\n"
            f"Viewer Feedback Highlights: {audience_feedback_text}\n"
        )

        res = ollama_service.generate_structured_json(system_prompt, user_prompt)
        
        # Build structured model
        recommendations = []
        for r in res.get("recommendations", []):
            try:
                recommendations.append(VideoImprovementItem(
                    category=r.get("category", "Content Quality"),
                    priority=RecommendationPriority(r.get("priority", "Medium")),
                    observed_problem=r.get("observed_problem", "Pacing could be tightened"),
                    supporting_evidence=r.get("supporting_evidence", "Audience requests faster delivery"),
                    proposed_improvement=r.get("proposed_improvement", "Add visual chapter markers"),
                    expected_benefit=r.get("expected_benefit", "Improves viewer orientation"),
                    implementation_steps=r.get("implementation_steps", ["Edit video introduction"])
                ))
            except Exception:
                pass

        return VideoImprovementReport(
            video_id=video_title[:30],
            recommendations=recommendations,
            suggested_titles=res.get("suggested_titles", [
                f"How {video_title} Actually Works (Visual Guide)",
                f"Master {video_title} Step-by-Step",
                f"Why Everyone is Talking About {video_title}"
            ]),
            thumbnail_concepts=res.get("thumbnail_concepts", [
                "Split screen: Complex code vs Clean visual diagram",
                "Trainer pointing at glowing neural architecture diagram",
                "High-contrast 3D block with question mark and checkmark"
            ]),
            opening_hooks=res.get("opening_hooks", [
                "In the next 5 minutes, you'll understand what takes most engineers months to grasp.",
                "If you've ever wondered how this technology actually functions under the hood, watch this.",
                "Here is the single biggest misconception about this topic—and how to fix it."
            ]),
            chapter_plan=res.get("chapter_plan", [
                {"timestamp_approx": "00:00", "chapter_title": "The Hook & Problem Definition"},
                {"timestamp_approx": "01:30", "chapter_title": "Core Architecture & Principles"},
                {"timestamp_approx": "03:15", "chapter_title": "Real-World Practical Demonstration"},
                {"timestamp_approx": "04:30", "chapter_title": "Key Takeaways & Summary"}
            ])
        )

    def chat_response(
        self,
        message: str,
        conversation_history: List[Dict[str, str]],
        context_dict: Dict[str, Any]
    ) -> str:
        """
        Interactive Copilot conversation with bounded token budgeting.
        """
        sys_context = (
            "You are the AI Video Content Copilot for GenAI Video Intelligence Studio.\n"
            "You assist creators in improving educational video clarity, pacing, hook design, and visual animations.\n"
            f"Active Project Context:\n"
            f"- Title: {context_dict.get('title', 'Not specified')}\n"
            f"- Duration: {context_dict.get('duration', 'N/A')}s\n"
            f"- Recent Topics: {context_dict.get('topics', 'General AI and programming')}\n"
            f"- Sentiment Overview: {context_dict.get('sentiment', 'Positive audience engagement')}\n"
            "Answer questions concisely, professionally, and constructively."
        )

        messages = [{"role": "system", "content": sys_context}]
        # Keep last 6 conversation turns
        for turn in conversation_history[-6:]:
            messages.append(turn)
        messages.append({"role": "user", "content": message})

        return ollama_service.generate_chat(messages, temperature=0.3)

content_strategy_agent = ContentStrategyAgent()
