"""
Editing Planner Agent.
Generates structured Edit Decision Lists (EDL) using Llama 3.2 with strict schema validation
and an allowlist of editing operations. Does not execute arbitrary shell commands.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import json
from models.editing_models import EditDecisionList, EditOperation, EditOperationType
from models.schemas import TranscriptionResult
from services.ollama_service import ollama_service
from services.video_service import video_service
from utils.logging_config import logger

class EditingAgent:
    def __init__(self):
        pass

    def generate_edit_plan(
        self,
        job_id: str,
        video_path: Path,
        duration_sec: float,
        transcription: Optional[TranscriptionResult] = None,
        scenes: Optional[List[Dict[str, Any]]] = None
    ) -> EditDecisionList:
        """
        Synthesize an Edit Decision List (EDL) using Llama 3.2.
        Preserves educational explanations and equations while trimming dead pauses.
        """
        # Prepare context
        transcript_sample = transcription.text[:800] if transcription else "Educational explanation"
        
        system_prompt = (
            "You are an expert educational video editor.\n"
            "Generate a structured Edit Decision List (EDL) for an educational lecture.\n"
            "RULES:\n"
            "1. Preserve ALL important technical explanations, formulas, code demos, and teacher speech.\n"
            "2. Identify any excessive dead pauses (> 3.5 seconds) for trimming with 'CUT_PAUSE'.\n"
            "3. The primary video content MUST be kept with 'KEEP' operations.\n"
            "4. Supported operation types: 'KEEP', 'CUT_PAUSE', 'CUT_REDUNDANT', 'INSERT_ANIMATION', 'OVERLAY_ENGAGEMENT', 'BURN_CAPTIONS'.\n"
            "5. Return a JSON object with:\n"
            "   - 'operations': array of objects with keys: 'op_type', 'start_sec', 'end_sec', 'reason'\n"
            f"6. 'start_sec' and 'end_sec' MUST be within 0.0 and {duration_sec:.1f}.\n"
            "7. Return valid JSON only."
        )

        user_prompt = (
            f"Source video duration: {duration_sec:.1f} seconds.\n"
            f"Speech transcript preview: {transcript_sample}\n"
            "Generate the EDL plan preserving educational integrity."
        )

        operations: List[EditOperation] = []
        try:
            res = ollama_service.generate_structured_json(system_prompt, user_prompt)
            raw_ops = res.get("operations", [])
            for op in raw_ops:
                op_type_str = str(op.get("op_type", "KEEP")).upper()
                if op_type_str in [e.value for e in EditOperationType]:
                    s = max(0.0, float(op.get("start_sec", 0.0)))
                    e = min(duration_sec, float(op.get("end_sec", duration_sec)))
                    if e > s:
                        operations.append(EditOperation(
                            op_type=EditOperationType(op_type_str),
                            start_sec=round(s, 2),
                            end_sec=round(e, 2),
                            reason=str(op.get("reason", "Standard edit cut"))
                        ))
        except Exception as e:
            logger.warning(f"LLM EDL generation fallback: {e}")

        # If LLM returned empty or invalid operations, generate safe default keep plan
        if not operations or not any(op.op_type == EditOperationType.KEEP for op in operations):
            operations = [
                EditOperation(
                    op_type=EditOperationType.KEEP,
                    start_sec=0.0,
                    end_sec=round(duration_sec, 2),
                    reason="Preserve complete educational lecture content"
                ),
                EditOperation(
                    op_type=EditOperationType.OVERLAY_ENGAGEMENT,
                    start_sec=round(min(15.0, duration_sec * 0.2), 2),
                    end_sec=round(min(20.0, duration_sec * 0.2 + 5.0), 2),
                    reason="Introductory engagement overlay"
                )
            ]

        target_duration = sum(op.end_sec - op.start_sec for op in operations if op.op_type == EditOperationType.KEEP)

        edl = EditDecisionList(
            job_id=job_id,
            source_media_path=str(video_path),
            source_duration_sec=round(duration_sec, 2),
            target_duration_sec=round(target_duration, 2),
            operations=operations
        )
        return edl

    def execute_edit_plan(self, edl: EditDecisionList, output_path: Path, work_dir: Path) -> Path:
        """Render the EDL safely via VideoService."""
        return video_service.render_edl(edl, output_path, work_dir)

editing_agent = EditingAgent()
