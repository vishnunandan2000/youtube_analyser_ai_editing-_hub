"""
Educational Study Notes Service.
Generates structured A4 PDF notes with notebook styling and renders page preview images via PyMuPDF.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import fitz  # PyMuPDF
from models.schemas import NoteSection
from utils.logging_config import logger

class NumberedCanvas(canvas.Canvas):
    """Custom canvas to draw notebook margins, lined paper styling, and page numbers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages: int):
        self.saveState()
        w, h = A4

        # Red left margin line (classic student notebook style)
        self.setStrokeColor(colors.HexColor("#F43F5E"))
        self.setLineWidth(1.2)
        self.line(54, 40, 54, h - 40)

        # Light notebook horizontal ruling lines
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        for y in range(60, int(h - 60), 22):
            self.line(60, y, w - 40, y)

        # Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(60, h - 35, "GENAI VIDEO INTELLIGENCE STUDIO — STUDY & REVISION NOTES")

        # Footer page number
        self.setFont("Helvetica", 9)
        self.drawRightString(w - 40, 25, f"Page {self._pageNumber} of {total_pages}")
        self.restoreState()


class NotesService:
    def __init__(self):
        pass

    def generate_pdf_notes(
        self,
        title: str,
        sections: List[NoteSection],
        output_pdf_path: Path,
        author: str = "GenAI Studio Educator",
        clean_printable_mode: bool = False
    ) -> Tuple[Path, List[Path]]:
        """
        Generate A4 PDF notes document and return the PDF path plus generated page preview PNGs.
        """
        output_pdf_path.parent.mkdir(parents=True, exist_ok=True)
        doc = SimpleDocTemplate(
            str(output_pdf_path),
            pagesize=A4,
            leftMargin=65,
            rightMargin=45,
            topMargin=55,
            bottomMargin=50
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#1E1B4B"),
            spaceAfter=12
        )
        sub_style = ParagraphStyle(
            "DocSub",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#64748B"),
            spaceAfter=18
        )
        heading_style = ParagraphStyle(
            "HeadingSection",
            parent=styles["Heading2"],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#4338CA"),
            spaceBefore=14,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            "BodyNotes",
            parent=styles["Normal"],
            fontSize=10,
            leading=15,
            textColor=colors.HexColor("#1E293B"),
            spaceAfter=6
        )
        code_style = ParagraphStyle(
            "CodeNotes",
            parent=styles["Code"],
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#0F172A"),
            backColor=colors.HexColor("#F1F5F9"),
            spaceBefore=4,
            spaceAfter=6
        )

        story = []
        # Title block
        story.append(Paragraph(f"📝 {title}", title_style))
        story.append(Paragraph(f"Curated Educational Synthesis • Instructor: {author}", sub_style))

        # Build sections
        for sec in sections:
            story.append(Paragraph(f"📌 {sec.heading}", heading_style))
            story.append(Paragraph(sec.content, body_style))

            if sec.key_points:
                story.append(Spacer(1, 4))
                for pt in sec.key_points:
                    bullet_text = f"<b>• Key Takeaway:</b> {pt}"
                    story.append(Paragraph(bullet_text, body_style))

            if sec.formulas_or_code:
                story.append(Spacer(1, 4))
                for snippet in sec.formulas_or_code:
                    story.append(Paragraph(f"<code>{snippet}</code>", code_style))

            if sec.diagram_concept:
                # Highlight callout box
                box_data = [[Paragraph(f"💡 <b>Mental Model / Concept Diagram:</b> {sec.diagram_concept}", body_style)]]
                t = Table(box_data, colWidths=[480])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FF")),
                    ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#6366F1")),
                    ('PADDING', (0,0), (-1,-1), 6),
                ]))
                story.append(Spacer(1, 4))
                story.append(t)

            story.append(Spacer(1, 10))

        # Build Document with custom NumberedCanvas or standard
        canvas_class = canvas.Canvas if clean_printable_mode else NumberedCanvas
        doc.build(story, canvasmaker=canvas_class)

        # Generate preview images for each page using PyMuPDF
        preview_images = self._render_pdf_to_images(output_pdf_path)
        return output_pdf_path, preview_images

    def _render_pdf_to_images(self, pdf_path: Path) -> List[Path]:
        """Convert PDF pages to PNG images for preview."""
        image_paths: List[Path] = []
        try:
            doc = fitz.open(str(pdf_path))
            out_dir = pdf_path.parent / f"{pdf_path.stem}_pages"
            out_dir.mkdir(parents=True, exist_ok=True)

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(dpi=150)
                img_path = out_dir / f"page_{page_num + 1}.png"
                pix.save(str(img_path))
                image_paths.append(img_path)
            doc.close()
        except Exception as e:
            logger.warning(f"Error rendering PDF pages to images: {e}")
        return image_paths

notes_service = NotesService()
