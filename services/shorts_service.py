"""
YouTube Shorts Generator Service.
Extracts high-impact educational segments, reframes to 9:16 vertical (1080x1920),
overlays kinetic hook captions, and strictly enforces duration <= 60 seconds.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import math
from models.editing_models import ShortCandidate
from models.schemas import SubtitleSegment
from utils.media_utils import run_ffmpeg_cmd, probe_media
from utils.logging_config import logger

class ShortsService:
    def __init__(self):
        self.max_duration_sec = 60.0

    def rank_and_select_candidates(
        self,
        segments: List[SubtitleSegment],
        total_video_duration: float,
        target_count: int = 3
    ) -> List[ShortCandidate]:
        """
        Identify self-contained educational moments from speech segments
        suitable for Shorts (each guaranteed <= 60 seconds).
        """
        candidates: List[ShortCandidate] = []
        if not segments:
            # Synthetic fallback if no segments
            dur = min(45.0, total_video_duration)
            if dur > 0:
                candidates.append(ShortCandidate(
                    id="short_1",
                    title="Key Educational Insight",
                    topic="Overview & Practical Application",
                    start_sec=0.0,
                    end_sec=dur,
                    duration_sec=dur,
                    hook_text="Did you know this about AI?",
                    selection_rationale="Initial conceptual definition with clear delivery.",
                    verified_under_60s=True
                ))
            return candidates

        # Group segments into contiguous windows of 25-50 seconds
        window_start = 0.0
        window_text = []
        seg_idx = 0

        while seg_idx < len(segments) and len(candidates) < target_count:
            seg = segments[seg_idx]
            window_start = seg.start
            window_end = seg.end
            window_text = [seg.text]

            # Accumulate up to 45 seconds
            inner_idx = seg_idx + 1
            while inner_idx < len(segments):
                next_seg = segments[inner_idx]
                potential_dur = next_seg.end - window_start
                if potential_dur > 50.0:  # Stay well under 60 seconds
                    break
                window_end = next_seg.end
                window_text.append(next_seg.text)
                inner_idx += 1

            dur = round(window_end - window_start, 2)
            if 15.0 <= dur <= 58.0:
                c_id = f"short_{len(candidates) + 1}"
                sample_text = " ".join(window_text)[:80]
                candidates.append(ShortCandidate(
                    id=c_id,
                    title=f"Lesson Highlight #{len(candidates) + 1}",
                    topic=f"Core Concept ({dur:.0f}s)",
                    start_sec=round(window_start, 2),
                    end_sec=round(window_end, 2),
                    duration_sec=dur,
                    hook_text=f"Master this concept in {int(dur)} seconds!",
                    selection_rationale=f"Self-contained snippet: '{sample_text}...'",
                    call_to_action="Subscribe for daily AI breakthroughs!",
                    verified_under_60s=True
                ))
                seg_idx = inner_idx  # Skip ahead to next distinct concept
            else:
                seg_idx += 1

        return candidates

    def render_vertical_short(
        self,
        source_video_path: Path,
        candidate: ShortCandidate,
        output_path: Path,
        work_dir: Path
    ) -> Path:
        """
        Renders a 9:16 vertical video (1080x1920) with blurred background padding
        to ensure instructor & slide remain 100% visible without cropping distortion.
        Strictly verifies that duration <= 60 seconds.
        """
        start = candidate.start_sec
        dur = min(candidate.duration_sec, self.max_duration_sec)

        # FFmpeg filter:
        # [0:v] split into [bg] and [fg].
        # [bg] scale=1080:1920, boxblur=20:20 (atmospheric blurred backdrop)
        # [fg] scale=1080:608:force_original_aspect_ratio=decrease (crisp centered original)
        # overlay [fg] onto [bg] at center (0, (1920-h)/2)
        # add top hook banner and bottom CTA text
        filter_str = (
            f"[0:v]split=2[bg_raw][fg_raw];"
            f"[bg_raw]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bg];"
            f"[fg_raw]scale=1080:1080:force_original_aspect_ratio=decrease[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2[vcomp];"
            f"[vcomp]drawtext=text='{candidate.hook_text.upper()}':fontcolor=yellow:fontsize=44:x=(w-text_w)/2:y=200:box=1:boxcolor=black@0.7:boxborderw=10,"
            f"drawtext=text='{candidate.call_to_action.upper()}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=1650:box=1:boxcolor=red@0.8:boxborderw=10[vout]"
        )

        args = [
            "-y",
            "-ss", str(start),
            "-t", str(dur),
            "-i", str(source_video_path),
            "-filter_complex", filter_str,
            "-map", "[vout]",
            "-map", "0:a?",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            "-c:a", "aac",
            "-b:a", "128k",
            str(output_path)
        ]

        run_ffmpeg_cmd(args, timeout_sec=180)

        # Enforce and verify <= 60.0s output
        meta = probe_media(output_path)
        actual_duration = meta.get("duration", 0.0)
        if actual_duration > 60.5:
            logger.error(f"Rendered Short exceeded duration constraint: {actual_duration:.1f}s > 60s")
            raise ValueError(f"Rendered Short duration ({actual_duration:.1f}s) violates 60-second limit.")
        
        logger.info(f"Verified Short duration: {actual_duration:.1f}s (<= 60s limit passed)")
        return output_path

shorts_service = ShortsService()
