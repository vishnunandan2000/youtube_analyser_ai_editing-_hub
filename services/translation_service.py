"""
Translation Service using Ollama Llama 3.2.
Supports 12 languages with preservation of technical keywords, code, and numerical terms.
"""

from typing import List, Dict, Any, Optional
import json
from models.schemas import SubtitleSegment
from services.ollama_service import ollama_service
from utils.logging_config import logger

SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "ta": "Tamil",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "bn": "Bengali",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ja": "Japanese"
}

class TranslationService:
    def __init__(self):
        self.supported_languages = SUPPORTED_LANGUAGES

    def translate_segments(
        self,
        segments: List[SubtitleSegment],
        target_lang_code: str,
        batch_size: int = 10
    ) -> List[SubtitleSegment]:
        """
        Translate a list of subtitle segments into target language preserving timing.
        """
        if target_lang_code.lower() == "en" or not segments:
            return segments

        lang_name = self.supported_languages.get(target_lang_code.lower(), target_lang_code)
        translated_segments: List[SubtitleSegment] = []

        system_prompt = (
            f"You are a professional educational and technical translator specializing in {lang_name}.\n"
            f"Translate the provided subtitle segments into natural, fluent {lang_name}.\n"
            "CRITICAL RULES:\n"
            "1. Preserve technical terminology (e.g., 'Generative AI', 'Neural Network', 'Transformer', 'Python', 'API', 'Docker', equations, code keywords) exactly as technical loan words or standard terminology.\n"
            "2. Keep mathematical formulas, numerals, and proper names intact.\n"
            "3. Return a JSON array of objects with keys: 'id' (integer) and 'text' (translated string).\n"
            "4. Respond with valid JSON only."
        )

        for i in range(0, len(segments), batch_size):
            batch = segments[i:i + batch_size]
            payload = [{"id": s.id, "text": s.text} for s in batch]
            user_prompt = f"Target Language: {lang_name}\nSegments to translate:\n{json.dumps(payload, ensure_ascii=False)}"

            try:
                res = ollama_service.generate_structured_json(system_prompt, user_prompt)
                items = res if isinstance(res, list) else res.get("items", res.get("segments", []))
                
                # Map back to original segments
                lookup = {}
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict) and "id" in item and "text" in item:
                            lookup[item["id"]] = item["text"]

                for orig in batch:
                    translated_text = lookup.get(orig.id, orig.text)
                    translated_segments.append(SubtitleSegment(
                        id=orig.id,
                        start=orig.start,
                        end=orig.end,
                        text=translated_text,
                        speaker=orig.speaker
                    ))
            except Exception as e:
                logger.error(f"Translation batch failed: {e}. Keeping original text.")
                for orig in batch:
                    translated_segments.append(orig)

        return translated_segments

translation_service = TranslationService()
