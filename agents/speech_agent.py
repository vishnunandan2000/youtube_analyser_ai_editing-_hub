"""
Speech Transcription Agent.
Coordinates audio extraction, whisper model execution, and subtitle timestamping.
"""

from pathlib import Path
from typing import Optional
from models.schemas import TranscriptionResult
from services.transcription_service import transcription_service
from utils.logging_config import logger

class SpeechAgent:
    def __init__(self):
        pass

    def process_speech(self, video_path: Path, work_dir: Path, language: Optional[str] = None) -> TranscriptionResult:
        """Extract audio and transcribe with sentence and word-level timestamps."""
        wav_path = work_dir / f"{video_path.stem}_audio.wav"
        transcription_service.extract_audio(video_path, wav_path)
        result = transcription_service.transcribe(wav_path, language=language)
        
        # Save SRT and VTT to work dir
        transcription_service.export_srt(result.segments, work_dir / f"{video_path.stem}.srt")
        transcription_service.export_vtt(result.segments, work_dir / f"{video_path.stem}.vtt")
        
        logger.info(f"Speech processing completed: {len(result.segments)} segments found.")
        return result

speech_agent = SpeechAgent()
