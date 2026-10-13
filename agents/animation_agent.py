"""
Animation Planning and Generation Agent.
Detects educational concepts from lecture transcripts and renders motion graphic assets.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from models.editing_models import AnimationCue
from services.animation_service import animation_service
from services.ollama_service import ollama_service
from utils.logging_config import logger

class AnimationPlanningAgent:
    def __init__(self):
        pass

    def identify_animation_cues(self, transcript_text: str, duration_sec: float) -> List[AnimationCue]:
        """
        Analyze transcript with Llama 3.2 to locate key moments requiring visual explanation.
        """
        system_prompt = (
            "You are an educational animation director.\n"
            "Analyze the transcript and identify 1-2 points where a motion graphic would enhance understanding.\n"
            "Supported animation types: 'ML_PIPELINE', 'NEURAL_NET', 'CYBER_PACKET', 'CONCEPT_CARD'.\n"
            "Return a JSON array of objects with keys:\n"
            "- 'id': string (e.g. 'anim_1')\n"
            "- 'concept': short concept title\n"
            "- 'animation_type': string from supported types\n"
            "- 'start_sec': float timestamp\n"
            "- 'end_sec': float timestamp (duration 4-8s)\n"
            "- 'labels': array of 3-4 stage labels\n"
            "- 'color_scheme': string\n"
            "Return valid JSON only."
        )

        user_prompt = f"Video Duration: {duration_sec}s. Transcript snippet: {transcript_text[:1000]}"
        cues: List[AnimationCue] = []

        try:
            res = ollama_service.generate_structured_json(system_prompt, user_prompt)
            items = res if isinstance(res, list) else res.get("items", res.get("cues", []))
            for item in items:
                if isinstance(item, dict) and "concept" in item:
                    s = max(0.0, float(item.get("start_sec", 10.0)))
                    e = min(duration_sec, float(item.get("end_sec", s + 5.0)))
                    cues.append(AnimationCue(
                        id=str(item.get("id", f"anim_{len(cues)+1}")),
                        concept=item.get("concept", "Core Technology"),
                        start_sec=round(s, 2),
                        end_sec=round(e, 2),
                        animation_type=item.get("animation_type", "CONCEPT_CARD"),
                        labels=item.get("labels", ["Input", "Processing", "Output"]),
                        color_scheme=item.get("color_scheme", "Electric Violet"),
                        narration_context=transcript_text[:100]
                    ))
        except Exception as e:
            logger.warning(f"Animation cue extraction fallback: {e}")

        if not cues:
            # Default cue
            cues.append(AnimationCue(
                id="anim_default",
                concept="Generative AI Workflow",
                start_sec=round(min(10.0, duration_sec * 0.2), 2),
                end_sec=round(min(16.0, duration_sec * 0.2 + 6.0), 2),
                animation_type="ML_PIPELINE",
                labels=["Training Data", "Foundation Model", "Fine-Tuning", "Inference"],
                color_scheme="Electric Violet"
            ))

        return cues

    def render_cue(self, cue: AnimationCue, output_path: Path, work_dir: Path) -> Path:
        """Render motion graphic clip."""
        dur = max(3.0, cue.end_sec - cue.start_sec)
        return animation_service.create_educational_animation(
            concept=cue.concept,
            animation_type=cue.animation_type,
            labels=cue.labels,
            duration_sec=dur,
            output_video_path=output_path,
            work_dir=work_dir
        )

animation_agent = AnimationPlanningAgent()
