"""
Caption Translation Agent.
Translates subtitle segments into selected target languages, preserving technical terminology.
"""

from typing import List, Dict
from models.schemas import SubtitleSegment
from services.translation_service import translation_service, SUPPORTED_LANGUAGES
from utils.logging_config import logger

class TranslationAgent:
    def __init__(self):
        self.supported_languages = SUPPORTED_LANGUAGES

    def translate(self, segments: List[SubtitleSegment], target_language_code: str) -> List[SubtitleSegment]:
        """Translate segments into target language."""
        logger.info(f"Translating {len(segments)} subtitle segments into '{target_language_code}'...")
        return translation_service.translate_segments(segments, target_language_code)

translation_agent = TranslationAgent()
