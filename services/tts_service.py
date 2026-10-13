"""
Text-to-Speech (TTS) Service for Multilingual Video Dubbing.
Uses edge-tts neural voices across 12 languages with offline pyttsx3 fallback.
"""

import asyncio
import os
from pathlib import Path
from typing import Dict, List, Optional
import pyttsx3
from utils.logging_config import logger
from utils.media_utils import run_ffmpeg_cmd

VOICE_MAP: Dict[str, str] = {
    "en": "en-US-GuyNeural",
    "hi": "hi-IN-MadhurNeural",
    "te": "te-IN-MohanNeural",
    "ta": "ta-IN-ValluvarNeural",
    "kn": "kn-IN-GaganNeural",
    "ml": "ml-IN-MidhunNeural",
    "mr": "mr-IN-ManoharNeural",
    "bn": "bn-IN-BashkarNeural",
    "es": "es-ES-AlvaroNeural",
    "fr": "fr-FR-HenriNeural",
    "de": "de-DE-ConradNeural",
    "ja": "ja-JP-KeitaNeural"
}

class TTSService:
    def __init__(self):
        self.voice_map = VOICE_MAP

    async def _generate_edge_tts(self, text: str, voice: str, output_path: Path) -> None:
        """Generate audio file via edge-tts."""
        import edge_tts
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(output_path))

    def synthesize_speech(
        self,
        text: str,
        lang_code: str,
        output_path: Path
    ) -> Path:
        """
        Synthesize speech into WAV or MP3 audio file.
        Attempts neural edge-tts first, falls back to local pyttsx3 if offline.
        """
        if not text or not text.strip():
            raise ValueError("Cannot synthesize empty text.")

        voice = self.voice_map.get(lang_code.lower(), "en-US-GuyNeural")
        temp_mp3 = output_path.with_suffix(".mp3")

        try:
            # Try edge-tts
            asyncio.run(self._generate_edge_tts(text, voice, temp_mp3))
            
            # If target was WAV, convert using FFmpeg
            if output_path.suffix.lower() == ".wav":
                run_ffmpeg_cmd(["-y", "-i", str(temp_mp3), "-ar", "16000", "-ac", "1", str(output_path)])
                if temp_mp3.exists():
                    temp_mp3.unlink()
            return output_path

        except Exception as e:
            logger.warning(f"edge-tts synthesis failed ({e}). Falling back to pyttsx3...")
            try:
                engine = pyttsx3.init()
                engine.setProperty("rate", 160)
                temp_wav = output_path.with_suffix(".wav")
                engine.save_to_file(text, str(temp_wav))
                engine.runAndWait()
                return temp_wav
            except Exception as ex:
                logger.error(f"pyttsx3 fallback also failed: {ex}")
                raise RuntimeError(f"All TTS providers failed: {ex}")

    def mix_dubbed_audio_with_video(
        self,
        original_video: Path,
        dubbed_audio: Path,
        output_video: Path,
        original_audio_volume: float = 0.15,
        dubbed_audio_volume: float = 1.0
    ) -> Path:
        """
        Mix dubbed voiceover with background video audio (with audio ducking)
        and export synchronized dubbed MP4.
        """
        # FFmpeg filter_complex amix with volume adjustments
        filter_str = (
            f"[0:a]volume={original_audio_volume}[orig];"
            f"[1:a]volume={dubbed_audio_volume}[dub];"
            f"[orig][dub]amix=inputs=2:duration=first:dropout_transition=2[aout]"
        )

        args = [
            "-y",
            "-i", str(original_video),
            "-i", str(dubbed_audio),
            "-filter_complex", filter_str,
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            str(output_video)
        ]

        run_ffmpeg_cmd(args, timeout_sec=300)
        return output_video

tts_service = TTSService()
