"""
Core data schemas for transcription, subtitles, and structured notes.
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class WordTimestamp(BaseModel):
    word: str
    start: float
    end: float
    probability: float = 1.0

class SubtitleSegment(BaseModel):
    id: int
    start: float
    end: float
    text: str
    words: Optional[List[WordTimestamp]] = None
    speaker: Optional[str] = "Speaker 1"

class TranscriptionResult(BaseModel):
    language: str = "en"
    duration: float = 0.0
    text: str = ""
    segments: List[SubtitleSegment] = Field(default_factory=list)

class Chapter(BaseModel):
    title: str
    start: float
    end: float
    summary: str = ""

class NoteSection(BaseModel):
    heading: str
    content: str
    key_points: List[str] = Field(default_factory=list)
    formulas_or_code: List[str] = Field(default_factory=list)
    diagram_concept: Optional[str] = None
