"""
Voice Generation and Audio Dubbing Agent.
Synthesizes translated speech and mixes with original background audio.
"""

from pathlib import Path
from typing import List, Optional
from models.schemas import SubtitleSegment
from services.tts_service import tts_service
from utils.logging_config import logger

class VoiceGenerationAgent:
    def __init__(self):
        pass

    def dub_video(
        self,
        video_path: Path,
        segments: List[SubtitleSegment],
        target_lang: str,
        output_video_path: Path,
        work_dir: Path,
        original_audio_volume: float = 0.2,
        dubbed_audio_volume: float = 1.0
    ) -> Path:
        """
        Synthesize translated segments and combine with video track.
        """
        combined_text = " ".join([s.text for s in segments if s.text.strip()])
        if not combined_text:
            combined_text = "Educational lecture translation in progress."

        dub_audio_path = work_dir / f"dubbed_{target_lang}.mp3"
        logger.info(f"Synthesizing voice in '{target_lang}'...")
        tts_service.synthesize_speech(combined_text, target_lang, dub_audio_path)

        logger.info(f"Mixing dubbed voice with video...")
        return tts_service.mix_dubbed_audio_with_video(
            original_video=video_path,
            dubbed_audio=dub_audio_path,
            output_video=output_video_path,
            original_audio_volume=original_audio_volume,
            dubbed_audio_volume=dubbed_audio_volume
        )

tts_agent = VoiceGenerationAgent()
