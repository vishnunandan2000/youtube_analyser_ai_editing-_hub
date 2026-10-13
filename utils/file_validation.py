"""
File and input validation helpers for security and stability.
"""

import re
from pathlib import Path
from typing import Optional, Tuple
from config import settings

ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"}
ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

def sanitize_filename(name: str) -> str:
    """Strip dangerous characters and prevent path traversal."""
    name = Path(name).name
    # Keep alphanumeric, hyphen, underscore, dot
    clean_name = re.sub(r"[^\w\.-]", "_", name)
    return clean_name or "uploaded_media.mp4"

def validate_video_file(file_path: Path) -> Tuple[bool, str]:
    """Validate existence, extension, and file size limits."""
    if not file_path.exists():
        return False, f"File does not exist: {file_path.name}"
    
    ext = file_path.suffix.lower()
    if ext not in ALLOWED_VIDEO_EXTENSIONS:
        return False, f"Unsupported video format '{ext}'. Allowed: {', '.join(sorted(ALLOWED_VIDEO_EXTENSIONS))}"
        
    size_mb = file_path.stat().st_size / (1024 * 1024)
    if size_mb > settings.max_upload_size_mb:
        return False, f"File size ({size_mb:.1f} MB) exceeds maximum allowed limit of {settings.max_upload_size_mb} MB"
        
    return True, "Valid video file"

def extract_youtube_video_id(url: str) -> Optional[str]:
    """
    Safely extract YouTube video ID from various standard formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    """
    if not url or not isinstance(url, str):
        return None
    url = url.strip()
    
    patterns = [
        r"(?:v=|\/v\/|youtu\.be\/|\/embed\/|\/shorts\/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None
