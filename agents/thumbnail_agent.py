"""
Thumbnail Generation Agent.
Coordinates thumbnail concepts generation, title styling, and image export.
"""

from pathlib import Path
from typing import List, Optional
from services.thumbnail_service import thumbnail_service
from services.ollama_service import ollama_service
from utils.logging_config import logger

class ThumbnailAgent:
    def __init__(self):
        pass

    def generate_thumbnails(
        self,
        video_title: str,
        topic_summary: str,
        trainer_image_path: Optional[Path] = None,
        output_dir: Optional[Path] = None
    ) -> List[Path]:
        """
        Produce 3 distinct 1280x720 thumbnail designs.
        """
        # Refine short punchy title with Llama 3.2
        short_title = video_title
        if len(video_title) > 35:
            try:
                system_prompt = "You are a YouTube thumbnail copywriter. Convert the video title into a short, punchy 3-5 word headline for a thumbnail image. Respond with ONLY the short headline."
                headline = ollama_service.generate_chat([
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Title: {video_title}"}
                ], temperature=0.3).strip().replace('"', '')
                if headline and len(headline) < 40:
                    short_title = headline
            except Exception:
                pass

        logger.info(f"Generating 3 thumbnail concepts for '{short_title}'...")
        return thumbnail_service.generate_concepts(
            title=short_title,
            subtitle="IN 5 MINUTES",
            badge_text="AI MASTERCLASS",
            trainer_image_path=trainer_image_path,
            output_dir=output_dir
        )

thumbnail_agent = ThumbnailAgent()
