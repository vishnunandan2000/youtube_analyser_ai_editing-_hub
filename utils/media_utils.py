"""
Media utilities for FFmpeg and FFprobe binary management and safe execution.
"""

import os
import shutil
import subprocess
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from utils.logging_config import logger

# Initialize static_ffmpeg paths if available
try:
    import static_ffmpeg
    static_ffmpeg.add_paths()
    logger.info("static_ffmpeg paths initialized successfully.")
except Exception as e:
    logger.warning(f"Could not initialize static_ffmpeg paths: {e}")

def get_ffmpeg_path() -> Optional[str]:
    """Find the path to the ffmpeg executable."""
    path = shutil.which("ffmpeg")
    if not path:
        # Check standard static_ffmpeg locations on Windows
        base = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Python"
        for p in base.glob("**/static_ffmpeg/bin/*/ffmpeg.EXE"):
            if p.exists():
                return str(p)
    return path

def get_ffprobe_path() -> Optional[str]:
    """Find the path to the ffprobe executable."""
    path = shutil.which("ffprobe")
    if not path:
        base = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Python"
        for p in base.glob("**/static_ffmpeg/bin/*/ffprobe.EXE"):
            if p.exists():
                return str(p)
    return path

def run_ffmpeg_cmd(args: List[str], timeout_sec: int = 300) -> subprocess.CompletedProcess:
    """
    Safely execute FFmpeg commands with argument list (preventing shell injection).
    """
    ffmpeg_bin = get_ffmpeg_path()
    if not ffmpeg_bin:
        raise RuntimeError("FFmpeg executable not found. Please verify FFmpeg installation.")
    
    cmd = [ffmpeg_bin] + args
    logger.info(f"Executing FFmpeg: {' '.join(cmd[:10])} ...")
    
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_sec,
            check=True
        )
        return proc
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg error: {e.stderr[:500] if e.stderr else str(e)}")
        raise RuntimeError(f"FFmpeg processing failed: {e.stderr[:300] if e.stderr else str(e)}")
    except subprocess.TimeoutExpired:
        logger.error(f"FFmpeg command timed out after {timeout_sec} seconds")
        raise TimeoutError(f"FFmpeg processing timed out ({timeout_sec}s)")

def probe_media(file_path: Path) -> Dict[str, Any]:
    """
    Inspect media container, streams, duration, resolution, codecs using FFprobe.
    """
    ffprobe_bin = get_ffprobe_path()
    if not ffprobe_bin:
        raise RuntimeError("FFprobe executable not found.")
    
    if not file_path.exists():
        raise FileNotFoundError(f"Media file not found: {file_path}")
        
    cmd = [
        ffprobe_bin,
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        str(file_path)
    ]
    
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    data = json.loads(proc.stdout)
    
    format_info = data.get("format", {})
    streams = data.get("streams", [])
    
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
    
    duration = float(format_info.get("duration", 0.0))
    width = int(video_stream.get("width", 0)) if video_stream else 0
    height = int(video_stream.get("height", 0)) if video_stream else 0
    
    # Calculate FPS safely
    fps = 30.0
    if video_stream and "r_frame_rate" in video_stream:
        r_parts = video_stream["r_frame_rate"].split("/")
        if len(r_parts) == 2 and float(r_parts[1]) > 0:
            fps = round(float(r_parts[0]) / float(r_parts[1]), 2)
            
    return {
        "filename": file_path.name,
        "path": str(file_path),
        "duration": duration,
        "size_bytes": int(format_info.get("size", file_path.stat().st_size)),
        "bitrate": int(format_info.get("bit_rate", 0)),
        "has_video": video_stream is not None,
        "has_audio": audio_stream is not None,
        "width": width,
        "height": height,
        "fps": fps,
        "video_codec": video_stream.get("codec_name", "none") if video_stream else "none",
        "audio_codec": audio_stream.get("codec_name", "none") if audio_stream else "none",
        "audio_sample_rate": int(audio_stream.get("sample_rate", 0)) if audio_stream else 0,
        "audio_channels": int(audio_stream.get("channels", 0)) if audio_stream else 0
    }
