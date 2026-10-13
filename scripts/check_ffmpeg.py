import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import shutil
from utils.media_utils import get_ffmpeg_path, get_ffprobe_path, run_ffmpeg_cmd

def check_ffmpeg():
    print("=" * 60)
    print(" FFMPEG & MEDIA SUBSYSTEM DIAGNOSTIC")
    print("=" * 60)
    ffmpeg_bin = get_ffmpeg_path()
    ffprobe_bin = get_ffprobe_path()

    print(f"FFmpeg binary path:  {ffmpeg_bin}")
    print(f"FFprobe binary path: {ffprobe_bin}")

    if ffmpeg_bin:
        try:
            res = run_ffmpeg_cmd(["-version"], timeout_sec=5)
            version_line = res.stdout.splitlines()[0] if res.stdout else "Available"
            print(f"FFmpeg Version:      {version_line}")
        except Exception as e:
            print(f"Error running FFmpeg: {e}")
    else:
        print("[FAIL] FFmpeg not found!")

    print("=" * 60)

if __name__ == "__main__":
    check_ffmpeg()
