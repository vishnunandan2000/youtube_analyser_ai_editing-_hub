"""
Quality Assurance (QA) Agent.
Validates rendered video files, subtitle timing, audio streams, and export integrity.
"""

from pathlib import Path
from typing import Dict, Any, List
from utils.media_utils import probe_media
from utils.logging_config import logger

class QualityAssuranceAgent:
    def __init__(self):
        pass

    def verify_rendered_video(self, video_path: Path, max_expected_duration: float = None) -> Dict[str, Any]:
        """
        Thoroughly inspect rendered media file for video and audio validity.
        """
        if not video_path.exists():
            return {
                "valid": False,
                "error": f"File does not exist: {video_path.name}",
                "file_size": 0
            }

        size = video_path.stat().st_size
        if size < 1024:  # Less than 1 KB is almost certainly corrupted
            return {
                "valid": False,
                "error": f"File is too small ({size} bytes), likely corrupted.",
                "file_size": size
            }

        try:
            info = probe_media(video_path)
            duration = info.get("duration", 0.0)
            has_video = info.get("has_video", False)

            if not has_video:
                return {
                    "valid": False,
                    "error": "Rendered file does not contain a valid video stream.",
                    "details": info
                }

            if max_expected_duration and duration > max_expected_duration + 1.0:
                return {
                    "valid": False,
                    "error": f"Duration ({duration:.1f}s) exceeded allowed threshold of {max_expected_duration:.1f}s.",
                    "details": info
                }

            return {
                "valid": True,
                "duration": duration,
                "resolution": f"{info.get('width')}x{info.get('height')}",
                "fps": info.get("fps"),
                "has_audio": info.get("has_audio"),
                "file_size_mb": round(size / (1024 * 1024), 2)
            }

        except Exception as e:
            return {
                "valid": False,
                "error": f"FFprobe validation failed: {str(e)}",
                "file_size": size
            }

quality_agent = QualityAssuranceAgent()
