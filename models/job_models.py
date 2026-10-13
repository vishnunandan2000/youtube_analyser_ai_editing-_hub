"""
Pydantic models for background job tracking and export artifacts.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class JobStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class JobArtifact(BaseModel):
    name: str
    category: str  # "Video", "Subtitle", "Audio", "Document", "Image", "Data"
    file_path: str
    file_size_bytes: int = 0
    mime_type: str = "application/octet-stream"
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class VideoProcessingJob(BaseModel):
    job_id: str
    status: JobStatus = JobStatus.QUEUED
    stage: str = "Initialized"
    progress_pct: float = 0.0
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    duration_seconds: float = 0.0
    
    source_video_path: str = ""
    settings: Dict[str, Any] = Field(default_factory=dict)
    
    artifacts: List[JobArtifact] = Field(default_factory=list)
    error_message: Optional[str] = None
    stage_logs: List[str] = Field(default_factory=list)
    is_cancelled: bool = False
    
    def log_stage(self, stage_name: str, progress: float) -> None:
        self.stage = stage_name
        self.progress_pct = min(100.0, max(0.0, progress))
        self.updated_at = datetime.utcnow().isoformat()
        log_entry = f"[{self.updated_at}] {stage_name} ({self.progress_pct:.0f}%)"
        self.stage_logs.append(log_entry)
