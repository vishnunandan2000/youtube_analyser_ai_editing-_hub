"""
Pydantic models for video editing operations, Edit Decision List (EDL), and Shorts generation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class EditOperationType(str, Enum):
    KEEP = "KEEP"
    CUT_PAUSE = "CUT_PAUSE"
    CUT_REDUNDANT = "CUT_REDUNDANT"
    INSERT_ANIMATION = "INSERT_ANIMATION"
    OVERLAY_ENGAGEMENT = "OVERLAY_ENGAGEMENT"
    BURN_CAPTIONS = "BURN_CAPTIONS"
    AUDIO_DUCKING = "AUDIO_DUCKING"
    TRANSITION = "TRANSITION"

class EditOperation(BaseModel):
    op_type: EditOperationType
    start_sec: float
    end_sec: float
    reason: str = ""
    parameters: Dict[str, Any] = Field(default_factory=dict)

class EditDecisionList(BaseModel):
    job_id: str
    source_media_path: str
    source_duration_sec: float
    target_duration_sec: float
    operations: List[EditOperation] = Field(default_factory=list)
    created_at: str = ""

class AnimationCue(BaseModel):
    id: str
    concept: str
    start_sec: float
    end_sec: float
    animation_type: str  # "ML_PIPELINE", "NEURAL_NET", "CYBER_PACKET", "CODE_BLOCK", "CONCEPT_CARD", "LIKE_SUBSCRIBE"
    labels: List[str] = Field(default_factory=list)
    color_scheme: str = "Modern Dark / Electric Violet"
    narration_context: str = ""

class ShortCandidate(BaseModel):
    id: str
    title: str
    topic: str
    start_sec: float
    end_sec: float
    duration_sec: float
    hook_text: str
    selection_rationale: str
    call_to_action: str = "Follow for more AI insights!"
    verified_under_60s: bool = True
