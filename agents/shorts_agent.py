"""
Shorts Extraction and Production Agent.
Selects self-contained educational moments, renders 9:16 vertical videos,
and verifies strict <= 60 second duration constraints.
"""

from pathlib import Path
from typing import List, Tuple
from models.editing_models import ShortCandidate
from models.schemas import TranscriptionResult
from services.shorts_service import shorts_service
from utils.logging_config import logger

class ShortsExtractionAgent:
    def __init__(self):
        pass

    def produce_shorts(
        self,
        video_path: Path,
        duration_sec: float,
        transcription: TranscriptionResult,
        work_dir: Path,
        max_shorts: int = 2
    ) -> List[Tuple[ShortCandidate, Path]]:
        """
        Extract candidate educational highlights and render vertical Shorts <= 60s.
        """
        candidates = shorts_service.rank_and_select_candidates(
            segments=transcription.segments,
            total_video_duration=duration_sec,
            target_count=max_shorts
        )

        rendered_shorts: List[Tuple[ShortCandidate, Path]] = []
        for i, candidate in enumerate(candidates):
            short_out = work_dir / f"short_{candidate.id}_{i+1}.mp4"
            logger.info(f"Rendering Short {candidate.id} ({candidate.duration_sec:.1f}s)...")
            try:
                out_path = shorts_service.render_vertical_short(
                    source_video_path=video_path,
                    candidate=candidate,
                    output_path=short_out,
                    work_dir=work_dir
                )
                rendered_shorts.append((candidate, out_path))
            except Exception as e:
                logger.error(f"Failed to render Short {candidate.id}: {e}")

        return rendered_shorts

shorts_agent = ShortsExtractionAgent()
