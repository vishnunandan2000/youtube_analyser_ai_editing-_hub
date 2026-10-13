"""
Project Orchestrator Agent.
Coordinates all specialized agents in an end-to-end autonomous video production pipeline.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import uuid
from config import settings
from services.storage_service import storage_service
from agents.speech_agent import speech_agent
from agents.video_understanding_agent import video_understanding_agent
from agents.editing_agent import editing_agent
from agents.translation_agent import translation_agent
from agents.tts_agent import tts_agent
from agents.animation_agent import animation_agent
from agents.thumbnail_agent import thumbnail_agent
from agents.notes_agent import notes_agent
from agents.shorts_agent import shorts_agent
from agents.quality_agent import quality_agent
from utils.file_validation import validate_video_file, sanitize_filename
from utils.logging_config import logger

class ProjectOrchestrator:
    def __init__(self):
        pass

    def run_full_production_pipeline(
        self,
        video_input_path: str,
        trainer_image_path: Optional[str] = None,
        source_language: str = "auto",
        target_language: str = "en",
        output_resolution: str = "720p",
        output_fps: str = "30 fps",
        edit_style: str = "Educational Gentle",
        subtitle_style: str = "Classic White with Shadow",
        animation_intensity: str = "Standard",
        export_format: str = "mp4",
        bg_music: bool = False,
        original_volume: float = 0.2,
        dubbed_volume: float = 1.0,
        generate_shorts: bool = True,
        generate_thumbnails: bool = True,
        generate_notes: bool = True,
        generate_animations: bool = True,
        burn_captions: bool = True,
        custom_channel_name: str = "AI Creator Hub"
    ) -> Dict[str, Any]:
        """
        Execute full autonomous video production workflow.
        """
        source_path = Path(video_input_path)
        is_valid, msg = validate_video_file(source_path)
        if not is_valid:
            raise ValueError(msg)

        job_id = f"job_{uuid.uuid4().hex[:10]}"
        job_dir = settings.jobs_dir / job_id
        job_dir.mkdir(parents=True, exist_ok=True)

        job = storage_service.create_job(job_id, str(source_path), {
            "source_language": source_language,
            "target_language": target_language,
            "output_resolution": output_resolution,
            "output_fps": output_fps,
            "edit_style": edit_style,
            "subtitle_style": subtitle_style,
            "animation_intensity": animation_intensity,
            "export_format": export_format,
            "bg_music": bg_music,
            "original_volume": original_volume,
            "dubbed_volume": dubbed_volume,
            "generate_shorts": generate_shorts,
            "generate_thumbnails": generate_thumbnails,
            "generate_notes": generate_notes,
            "generate_animations": generate_animations
        })

        try:
            # 1. Media Inspection & Audio Extraction
            storage_service.update_job_stage(job_id, "Inspecting media and extracting audio", 10.0)
            visual_data = video_understanding_agent.analyze_visual_structure(source_path, job_dir)
            media_info = visual_data["media_info"]
            duration = media_info.get("duration", 0.0)

            # 2. Speech Transcription
            storage_service.update_job_stage(job_id, "Transcribing speech with faster-whisper", 25.0)
            transcription = speech_agent.process_speech(source_path, job_dir, language=source_language)
            
            # Register SRT and VTT
            srt_path = job_dir / f"{source_path.stem}.srt"
            vtt_path = job_dir / f"{source_path.stem}.vtt"
            if srt_path.exists():
                storage_service.register_artifact(job_id, "Original Subtitles (SRT)", "Subtitle", srt_path, "text/plain")
            if vtt_path.exists():
                storage_service.register_artifact(job_id, "Original Subtitles (VTT)", "Subtitle", vtt_path, "text/vtt")

            # 3. EDL Synthesis & Video Cutting
            storage_service.update_job_stage(job_id, "Generating Edit Decision List (EDL) with Llama 3.2", 40.0)
            edl = editing_agent.generate_edit_plan(
                job_id=job_id,
                video_path=source_path,
                duration_sec=duration,
                transcription=transcription,
                scenes=visual_data.get("scenes")
            )
            
            edited_video = job_dir / f"{source_path.stem}_edited.mp4"
            editing_agent.execute_edit_plan(edl, edited_video, job_dir)
            storage_service.register_artifact(job_id, "Edited Master Video", "Video", edited_video, "video/mp4")

            # 4. Optional Subtitle Burning
            final_rendered_video = edited_video
            if burn_captions and srt_path.exists():
                storage_service.update_job_stage(job_id, "Burning synchronized subtitles into video", 55.0)
                captioned_video = job_dir / f"{source_path.stem}_captioned.mp4"
                try:
                    from services.video_service import video_service
                    video_service.burn_subtitles(edited_video, srt_path, captioned_video, style=subtitle_style)
                    storage_service.register_artifact(job_id, "Captioned Video", "Video", captioned_video, "video/mp4")
                    final_rendered_video = captioned_video
                except Exception as e:
                    logger.warning(f"Subtitle burn-in skipped due to: {e}")

            # 5. Multilingual Translation & Dubbing
            if target_language != "en":
                storage_service.update_job_stage(job_id, f"Translating subtitles and dubbing voice into {target_language.upper()}", 65.0)
                translated_segments = translation_agent.translate(transcription.segments, target_language)
                dubbed_video_path = job_dir / f"{source_path.stem}_dubbed_{target_language}.mp4"
                try:
                    tts_agent.dub_video(
                        video_path=final_rendered_video,
                        segments=translated_segments,
                        target_lang=target_language,
                        output_video_path=dubbed_video_path,
                        work_dir=job_dir,
                        original_audio_volume=original_volume,
                        dubbed_audio_volume=dubbed_volume
                    )
                    storage_service.register_artifact(job_id, f"Dubbed Video ({target_language.upper()})", "Video", dubbed_video_path, "video/mp4")
                except Exception as e:
                    logger.warning(f"Voice dubbing skipped due to: {e}")

            # 6. Context-Aware Motion Graphics
            if generate_animations:
                storage_service.update_job_stage(job_id, "Generating educational motion graphics and engagement overlays", 75.0)
                cues = animation_agent.identify_animation_cues(transcription.text, duration)
                if cues:
                    anim_out = job_dir / "educational_animation_clip.mp4"
                    animation_agent.render_cue(cues[0], anim_out, job_dir)
                    storage_service.register_artifact(job_id, f"Educational Animation ({cues[0].concept})", "Video", anim_out, "video/mp4")

            # 7. AI Thumbnails (3 Concepts)
            if generate_thumbnails:
                storage_service.update_job_stage(job_id, "Designing AI YouTube thumbnail concepts (1280x720)", 85.0)
                trainer_p = Path(trainer_image_path) if trainer_image_path else None
                thumb_paths = thumbnail_agent.generate_thumbnails(
                    video_title=source_path.stem.replace("_", " ").title(),
                    topic_summary=transcription.text[:100],
                    trainer_image_path=trainer_p,
                    output_dir=job_dir
                )
                for idx, tp in enumerate(thumb_paths, 1):
                    storage_service.register_artifact(job_id, f"Thumbnail Concept #{idx}", "Image", tp, "image/png")

            # 8. Educational Notes PDF
            if generate_notes:
                storage_service.update_job_stage(job_id, "Compiling handwritten-style study notes PDF", 92.0)
                notes_pdf = job_dir / f"{source_path.stem}_study_notes.pdf"
                pdf_path, page_images = notes_agent.create_notes_from_transcript(
                    video_title=source_path.stem.replace("_", " ").title(),
                    transcription=transcription,
                    output_pdf_path=notes_pdf
                )
                storage_service.register_artifact(job_id, "Educational Study Notes (PDF)", "Document", pdf_path, "application/pdf")

            # 9. YouTube Shorts (Verified <= 60s)
            if generate_shorts:
                storage_service.update_job_stage(job_id, "Extracting and rendering vertical YouTube Shorts (<=60s)", 97.0)
                shorts_list = shorts_agent.produce_shorts(
                    video_path=source_path,
                    duration_sec=duration,
                    transcription=transcription,
                    work_dir=job_dir,
                    max_shorts=1
                )
                for c_item, s_path in shorts_list:
                    # QA verification
                    qa_res = quality_agent.verify_rendered_video(s_path, max_expected_duration=60.0)
                    if qa_res["valid"]:
                        storage_service.register_artifact(job_id, f"YouTube Short ({c_item.title})", "Video", s_path, "video/mp4")

            # Mark Completed
            storage_service.mark_completed(job_id)
            final_job = storage_service.get_job(job_id)

            return {
                "success": True,
                "job_id": job_id,
                "job": final_job,
                "message": "Autonomous video production pipeline executed successfully."
            }

        except Exception as e:
            logger.error(f"Job {job_id} encountered critical error: {e}")
            storage_service.mark_failed(job_id, str(e))
            raise e

orchestrator = ProjectOrchestrator()
