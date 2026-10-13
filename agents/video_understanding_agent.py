"""
Video Understanding Agent.
Detects scene boundaries, extracts keyframes, and identifies candidate animation insertion points.
"""

from pathlib import Path
from typing import List, Dict, Any
from services.video_service import video_service
from utils.logging_config import logger

class VideoUnderstandingAgent:
    def __init__(self):
        pass

    def analyze_visual_structure(self, video_path: Path, work_dir: Path) -> Dict[str, Any]:
        """
        Extract scene transitions, sample keyframes, and locate visual pause points.
        """
        media_info = video_service.inspect_video(video_path)
        scenes = video_service.detect_scenes(video_path)

        keyframes_dir = work_dir / "keyframes"
        keyframes_dir.mkdir(parents=True, exist_ok=True)

        sampled_keyframes = []
        for i, sc in enumerate(scenes[:8]):  # Sample up to 8 keyframes
            kf_time = sc["keyframe_sec"]
            kf_path = keyframes_dir / f"keyframe_{i:02d}_{int(kf_time)}s.jpg"
            try:
                video_service.extract_frame_at_time(video_path, kf_time, kf_path)
                sampled_keyframes.append({
                    "timestamp": kf_time,
                    "path": str(kf_path),
                    "scene_index": i
                })
            except Exception as e:
                logger.warning(f"Failed to extract frame at {kf_time}s: {e}")

        logger.info(f"Video understanding complete: {len(scenes)} scenes detected, {len(sampled_keyframes)} keyframes sampled.")
        return {
            "media_info": media_info,
            "scenes": scenes,
            "keyframes": sampled_keyframes,
            "animation_insertion_candidates": [sc["start"] for sc in scenes if sc["end"] - sc["start"] > 4.0]
        }

video_understanding_agent = VideoUnderstandingAgent()
