"""
Speech Transcription Service using faster-whisper.
Extracts audio from video, generates sentence and word-level timestamps, and exports SRT/VTT.
"""

from pathlib import Path
from typing import List, Optional, Tuple
import os
from models.schemas import TranscriptionResult, SubtitleSegment, WordTimestamp
from utils.media_utils import run_ffmpeg_cmd
from utils.timestamp_utils import seconds_to_srt_time, seconds_to_vtt_time
from utils.logging_config import logger

class TranscriptionService:
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self._model = None

    def _get_model(self):
        if self._model is None:
            try:
                from faster_whisper import WhisperModel
                logger.info(f"Loading faster-whisper model ({self.model_size})...")
                # CPU int8 is fast, lightweight, and universally supported across Windows hardware
                self._model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
            except Exception as e:
                logger.error(f"Failed to initialize faster-whisper: {e}")
                raise RuntimeError(f"Could not load faster-whisper model: {e}")
        return self._model

    def extract_audio(self, video_path: Path, output_wav_path: Optional[Path] = None) -> Path:
        """Extract a 16kHz mono WAV audio file from the video using FFmpeg."""
        if output_wav_path is None:
            output_wav_path = video_path.parent / f"{video_path.stem}_audio_16k.wav"

        args = [
            "-y",
            "-i", str(video_path),
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            str(output_wav_path)
        ]
        run_ffmpeg_cmd(args, timeout_sec=120)
        return output_wav_path

    def transcribe(self, audio_path: Path, language: Optional[str] = None) -> TranscriptionResult:
        """Transcribe audio file into structured segments with timestamps."""
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        try:
            model = self._get_model()
            lang_param = None
            if language and language != "auto" and "auto" not in language.lower():
                # Extract 2-letter ISO code if formatted like "en (English)"
                lang_param = language.split()[0].strip()

            segments_gen, info = model.transcribe(
                str(audio_path),
                beam_size=5,
                word_timestamps=True,
                vad_filter=True,
                language=lang_param
            )

            segments: List[SubtitleSegment] = []
            full_text_parts = []
            seg_id = 1

            for s in segments_gen:
                words_list = []
                if s.words:
                    for w in s.words:
                        words_list.append(WordTimestamp(
                            word=w.word,
                            start=round(w.start, 3),
                            end=round(w.end, 3),
                            probability=round(w.probability, 3)
                        ))

                text_clean = s.text.strip()
                if not text_clean:
                    continue

                segment_item = SubtitleSegment(
                    id=seg_id,
                    start=round(s.start, 3),
                    end=round(s.end, 3),
                    text=text_clean,
                    words=words_list
                )
                segments.append(segment_item)
                full_text_parts.append(text_clean)
                seg_id += 1

            return TranscriptionResult(
                language=info.language,
                duration=round(info.duration, 2),
                text=" ".join(full_text_parts),
                segments=segments
            )

        except Exception as e:
            logger.error(f"Transcription error: {e}")
            # Fallback for synthetic/empty audio
            return TranscriptionResult(
                language="en",
                duration=0.0,
                text="[Audio transcription could not be completed]",
                segments=[]
            )

    def export_srt(self, segments: List[SubtitleSegment], output_path: Path) -> Path:
        """Export subtitle segments as standard SubRip (.srt) file."""
        lines = []
        for i, seg in enumerate(segments, 1):
            lines.append(str(i))
            lines.append(f"{seconds_to_srt_time(seg.start)} --> {seconds_to_srt_time(seg.end)}")
            lines.append(seg.text)
            lines.append("")
        output_path.write_text("\n".join(lines), encoding="utf-8")
        return output_path

    def export_vtt(self, segments: List[SubtitleSegment], output_path: Path) -> Path:
        """Export subtitle segments as WebVTT (.vtt) file."""
        lines = ["WEBVTT", ""]
        for i, seg in enumerate(segments, 1):
            lines.append(str(i))
            lines.append(f"{seconds_to_vtt_time(seg.start)} --> {seconds_to_vtt_time(seg.end)}")
            lines.append(seg.text)
            lines.append("")
        output_path.write_text("\n".join(lines), encoding="utf-8")
        return output_path

transcription_service = TranscriptionService()
