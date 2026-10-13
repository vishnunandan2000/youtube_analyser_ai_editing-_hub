"""
AI Thumbnail Generation Service.
Generates YouTube 1280x720 thumbnails across 3 rich design concepts using Pillow.
"""

from pathlib import Path
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from utils.logging_config import logger

class ThumbnailService:
    def __init__(self):
        self.width = 1280
        self.height = 720

    def generate_concepts(
        self,
        title: str,
        subtitle: str = "COMPLETE MASTERCLASS",
        badge_text: str = "GENAI STUDIO",
        trainer_image_path: Optional[Path] = None,
        output_dir: Optional[Path] = None
    ) -> List[Path]:
        """
        Generate 3 distinct YouTube thumbnail concepts at 1280x720 resolution:
        1. High-Impact Cyber Tech
        2. Minimalist Executive Modern
        3. High-Energy Vibrant Explainer
        """
        if output_dir is None:
            from config import settings
            output_dir = settings.exports_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        concepts = []
        concepts.append(self._create_tech_concept(title, subtitle, badge_text, trainer_image_path, output_dir / "thumbnail_concept_1.png"))
        concepts.append(self._create_executive_concept(title, subtitle, badge_text, trainer_image_path, output_dir / "thumbnail_concept_2.png"))
        concepts.append(self._create_explainer_concept(title, subtitle, badge_text, trainer_image_path, output_dir / "thumbnail_concept_3.png"))
        return concepts

    def _create_tech_concept(self, title: str, subtitle: str, badge: str, trainer_img: Optional[Path], out_path: Path) -> Path:
        """Concept 1: High-Impact Cyber Tech (Dark Indigo, Neon Cyan & Purple Accents)."""
        img = Image.new("RGBA", (self.width, self.height), (10, 14, 26, 255))
        draw = ImageDraw.Draw(img)

        # Gradient background glow
        for r in range(400, 0, -20):
            alpha = int(25 * (1 - r / 400))
            draw.ellipse([(800 - r, 300 - r), (800 + r, 300 + r)], fill=(99, 102, 241, alpha))

        # Geometric Grid Accent
        for x in range(0, self.width, 80):
            draw.line([(x, 0), (x, self.height)], fill=(30, 41, 59, 100), width=1)

        # Outer Neon Border
        draw.rectangle([(20, 20), (self.width - 20, self.height - 20)], outline=(129, 140, 248, 200), width=4)

        # Badge Pill
        draw.rounded_rectangle([(70, 70), (320, 120)], radius=15, fill=(79, 70, 229, 255))
        draw.text((95, 82), badge.upper(), fill=(255, 255, 255, 255))

        # Main Title (Split into 2-3 lines if long)
        self._draw_wrapped_text(draw, title.upper(), 70, 160, max_w=750, font_size=56, text_color=(255, 255, 255), shadow_color=(0, 0, 0))

        # Subtitle
        draw.text((70, 520), subtitle.upper(), fill=(56, 189, 248, 255))

        # Bottom Bar
        draw.rectangle([(70, 570), (500, 576)], fill=(244, 63, 94, 255))

        # Overlay Trainer Image / Avatar if provided
        if trainer_img and trainer_img.exists():
            self._composite_subject_image(img, trainer_img, (820, 120), (400, 500))

        img.convert("RGB").save(out_path, quality=95)
        return out_path

    def _create_executive_concept(self, title: str, subtitle: str, badge: str, trainer_img: Optional[Path], out_path: Path) -> Path:
        """Concept 2: Minimalist Executive Modern (Charcoal, Crisp White, Emerald Accent)."""
        img = Image.new("RGBA", (self.width, self.height), (17, 24, 39, 255))
        draw = ImageDraw.Draw(img)

        # Diagonal accent block
        draw.polygon([(780, 0), (self.width, 0), (self.width, self.height), (650, self.height)], fill=(31, 41, 55, 255))

        # Emerald Accent Line
        draw.line([(650, 0), (520, self.height)], fill=(16, 185, 129, 255), width=8)

        # Badge
        draw.rounded_rectangle([(70, 80), (280, 125)], radius=10, fill=(16, 185, 129, 255))
        draw.text((90, 92), badge.upper(), fill=(0, 0, 0, 255))

        # Title
        self._draw_wrapped_text(draw, title, 70, 170, max_w=580, font_size=52, text_color=(249, 250, 251), shadow_color=(10, 10, 10))

        # Subtitle
        draw.text((70, 510), subtitle.upper(), fill=(156, 163, 175, 255))

        if trainer_img and trainer_img.exists():
            self._composite_subject_image(img, trainer_img, (800, 100), (420, 520))

        img.convert("RGB").save(out_path, quality=95)
        return out_path

    def _create_explainer_concept(self, title: str, subtitle: str, badge: str, trainer_img: Optional[Path], out_path: Path) -> Path:
        """Concept 3: High-Energy Explainer (Vibrant Amber & Crimson, High Click-Through Rate)."""
        img = Image.new("RGBA", (self.width, self.height), (24, 18, 43, 255))
        draw = ImageDraw.Draw(img)

        # Radial Warm Glow
        for r in range(500, 0, -25):
            alpha = int(35 * (1 - r / 500))
            draw.ellipse([(300 - r, 360 - r), (300 + r, 360 + r)], fill=(245, 158, 11, alpha))

        # Red Headline Highlight Box
        draw.rounded_rectangle([(60, 60), (self.width - 60, 130)], radius=12, fill=(225, 29, 72, 255))
        draw.text((85, 75), f"🔥  {badge.upper()} — {subtitle.upper()}", fill=(255, 255, 255, 255))

        # Main Title (Yellow / White)
        self._draw_wrapped_text(draw, title.upper(), 70, 180, max_w=720, font_size=58, text_color=(254, 240, 138), shadow_color=(0, 0, 0))

        # "5 MINS EXPLAINED" Pill
        draw.rounded_rectangle([(70, 530), (380, 590)], radius=20, fill=(234, 179, 8, 255))
        draw.text((95, 545), "⚡ 100% PRACTICAL", fill=(0, 0, 0, 255))

        if trainer_img and trainer_img.exists():
            self._composite_subject_image(img, trainer_img, (830, 160), (390, 480))

        img.convert("RGB").save(out_path, quality=95)
        return out_path

    def _draw_wrapped_text(
        self,
        draw: ImageDraw.Draw,
        text: str,
        x: int,
        y: int,
        max_w: int,
        font_size: int,
        text_color: Tuple[int, int, int],
        shadow_color: Tuple[int, int, int]
    ):
        """Draw wrapped text with drop shadow to prevent text clipping."""
        words = text.split()
        lines = []
        current_line = []
        chars_per_line = max(15, int(max_w / (font_size * 0.55)))

        for word in words:
            if len(" ".join(current_line + [word])) <= chars_per_line:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))

        line_h = int(font_size * 1.25)
        for i, line in enumerate(lines[:4]):  # Max 4 lines
            ly = y + i * line_h
            # Shadow
            draw.text((x + 3, ly + 3), line, fill=(*shadow_color, 255))
            # Text
            draw.text((x, ly), line, fill=(*text_color, 255))

    def _composite_subject_image(self, bg_img: Image.Image, subject_path: Path, pos: Tuple[int, int], size: Tuple[int, int]):
        """Safely resize and composite uploaded trainer/logo image."""
        try:
            sub = Image.open(subject_path).convert("RGBA")
            sub.thumbnail(size, Image.Resampling.LANCZOS)
            bg_img.paste(sub, pos, sub)
        except Exception as e:
            logger.warning(f"Failed to composite subject image: {e}")

thumbnail_service = ThumbnailService()
