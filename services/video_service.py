"""
Video Service for media inspection, scene detection, EDL execution, and video rendering.
Uses OpenCV and FFmpeg safely with input parameter allowlisting.
"""

from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import cv2
import numpy as np
import subprocess
from utils.media_utils import run_ffmpeg_cmd, probe_media
from utils.logging_config import logger
from models.editing_models import EditDecisionList, EditOperation, EditOperationType

class VideoService:
    def __init__(self):
        pass

    def create_sample_demo_video(self, output_path: Path) -> Path:
        """
        Generate a clean synthetic 1280x720 educational video with slides and audio tone
        to enable immediate testing without requiring users to upload local files.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        filter_str = (
            "color=c=#0F172A:s=1280x720:d=12[bg];"
            "[bg]drawtext=text='GENAI MASTERCLASS\\: FOUNDATION MODELS':fontcolor=white:fontsize=44:x=(w-text_w)/2:y=220,"
            "drawtext=text='Attention(Q,K,V) = softmax(QK^T / sqrt(d_k))V':fontcolor=yellow:fontsize=32:x=(w-text_w)/2:y=340,"
            "drawtext=text='Instructor\\: GenAI Video Intelligence Studio':fontcolor=#94A3B8:fontsize=26:x=(w-text_w)/2:y=480[vout]"
        )
        args = [
            "-y",
            "-f", "lavfi",
            "-i", "sine=frequency=440:duration=12",
            "-filter_complex", filter_str,
            "-map", "[vout]",
            "-map", "0:a",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-c:a", "aac",
            "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            str(output_path)
        ]
        run_ffmpeg_cmd(args, timeout_sec=60)
        return output_path

    def inspect_video(self, video_path: Path) -> Dict[str, Any]:
        """Inspect video streams, resolution, fps, and codecs."""
        return probe_media(video_path)

    def detect_scenes(
        self,
        video_path: Path,
        threshold: float = 30.0,
        min_scene_len_sec: float = 2.0
    ) -> List[Dict[str, Any]]:
        """
        Detect scene transitions using OpenCV frame difference analysis.
        Returns list of scene cuts with timestamps.
        """
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            logger.warning(f"Could not open video with OpenCV: {video_path}")
            return [{"start": 0.0, "end": 10.0, "keyframe_sec": 0.0}]

        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        min_frames = int(min_scene_len_sec * fps)

        scenes = []
        prev_gray = None
        last_cut_frame = 0
        frame_idx = 0
        step = max(1, int(fps / 5))  # Sample 5 frames per second for speed

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % step == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.resize(gray, (160, 90))

                if prev_gray is not None:
                    diff = cv2.absdiff(gray, prev_gray)
                    score = np.mean(diff)

                    if score > threshold and (frame_idx - last_cut_frame) > min_frames:
                        start_time = round(last_cut_frame / fps, 2)
                        end_time = round(frame_idx / fps, 2)
                        scenes.append({
                            "start": start_time,
                            "end": end_time,
                            "keyframe_sec": round((start_time + end_time) / 2, 2)
                        })
                        last_cut_frame = frame_idx

                prev_gray = gray

            frame_idx += 1

        cap.release()

        # Final scene
        end_time = round(total_frames / fps, 2)
        start_time = round(last_cut_frame / fps, 2)
        if end_time > start_time:
            scenes.append({
                "start": start_time,
                "end": end_time,
                "keyframe_sec": round((start_time + end_time) / 2, 2)
            })

        return scenes or [{"start": 0.0, "end": max(5.0, round(total_frames / fps, 2)), "keyframe_sec": 0.0}]

    def extract_frame_at_time(self, video_path: Path, timestamp_sec: float, output_path: Path) -> Path:
        """Extract a single frame image at a specific timestamp using FFmpeg."""
        args = [
            "-y",
            "-ss", str(timestamp_sec),
            "-i", str(video_path),
            "-vframes", "1",
            "-q:v", "2",
            str(output_path)
        ]
        run_ffmpeg_cmd(args, timeout_sec=30)
        return output_path

    def render_edl(
        self,
        edl: EditDecisionList,
        output_path: Path,
        work_dir: Path
    ) -> Path:
        """
        Execute an Edit Decision List (EDL) using safe FFmpeg filter/concat.
        Keeps original video untouched.
        """
        source_path = Path(edl.source_media_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Source video not found: {source_path}")

        # Extract keep segments
        keep_segments: List[Tuple[float, float]] = []
        for op in edl.operations:
            if op.op_type == EditOperationType.KEEP:
                if op.end_sec > op.start_sec:
                    keep_segments.append((op.start_sec, op.end_sec))

        # If no explicit keeps, keep full duration
        if not keep_segments:
            keep_segments = [(0.0, edl.source_duration_sec)]

        # Cut individual segments
        segment_files: List[Path] = []
        for i, (start, end) in enumerate(keep_segments):
            dur = end - start
            seg_file = work_dir / f"seg_{i:03d}.mp4"
            args = [
                "-y",
                "-ss", str(start),
                "-t", str(dur),
                "-i", str(source_path),
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "22",
                "-c:a", "aac",
                "-b:a", "128k",
                "-avoid_negative_ts", "make_zero",
                str(seg_file)
            ]
            run_ffmpeg_cmd(args, timeout_sec=120)
            segment_files.append(seg_file)

        # Concat segments
        concat_list_file = work_dir / "concat_list.txt"
        with open(concat_list_file, "w", encoding="utf-8") as f:
            for sf in segment_files:
                f.write(f"file '{sf.as_posix()}'\n")

        args_concat = [
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list_file),
            "-c", "copy",
            str(output_path)
        ]
        run_ffmpeg_cmd(args_concat, timeout_sec=180)
        return output_path

    def burn_subtitles(self, video_path: Path, srt_path: Path, output_path: Path, style: str = "Classic White with Shadow") -> Path:
        """Burn subtitles into video using FFmpeg subtitles filter with clean styling."""
        srt_clean = str(srt_path).replace("\\", "/").replace(":", "\\:")
        if "Yellow" in style:
            force_style = "FontSize=22,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=3,Outline=2,Shadow=0,MarginV=35"
        elif "Lower-Third" in style or "Banner" in style:
            force_style = "FontSize=18,PrimaryColour=&H00F8FAFC,OutlineColour=&H80000000,BorderStyle=4,Outline=1,Shadow=1,MarginV=25"
        else:  # Classic White
            force_style = "FontSize=20,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,Outline=2,Shadow=1,MarginV=30"

        subtitle_filter = f"subtitles='{srt_clean}':force_style='{force_style}'"

        args = [
            "-y",
            "-i", str(video_path),
            "-vf", subtitle_filter,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "22",
            "-c:a", "copy",
            str(output_path)
        ]
        run_ffmpeg_cmd(args, timeout_sec=300)
        return output_path

video_service = VideoService()
