"""
Unit tests for file validation, path traversal prevention, and YouTube URL parsing.
"""

from pathlib import Path
from utils.file_validation import sanitize_filename, extract_youtube_video_id, validate_video_file

def test_sanitize_filename():
    assert sanitize_filename("../../../etc/passwd") == "passwd"
    assert sanitize_filename("my video file (1).mp4") == "my_video_file__1_.mp4"
    assert sanitize_filename("") == "uploaded_media.mp4"

def test_extract_youtube_video_id():
    # Standard watch
    assert extract_youtube_video_id("https://www.youtube.com/watch?v=NRmAXDWJVnU") == "NRmAXDWJVnU"
    # Short youtu.be
    assert extract_youtube_video_id("https://youtu.be/NRmAXDWJVnU?si=KrGLT1kBWlSe1Wzj") == "NRmAXDWJVnU"
    # Shorts URL
    assert extract_youtube_video_id("https://www.youtube.com/shorts/NRmAXDWJVnU") == "NRmAXDWJVnU"
    # Bare ID
    assert extract_youtube_video_id("NRmAXDWJVnU") == "NRmAXDWJVnU"
    # Invalid URLs
    assert extract_youtube_video_id("https://google.com") is None
    assert extract_youtube_video_id("") is None
