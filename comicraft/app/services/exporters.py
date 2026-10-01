from pathlib import Path
from uuid import uuid4
from fpdf import FPDF
from PIL import Image
from app.models import ComicPanel

BASE_DIR = Path(__file__).resolve().parent.parent.parent
EXPORT_DIR = BASE_DIR / "static" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def save_pdf(title: str, panels: list[ComicPanel]) -> str:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    for panel in panels:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, title[:80], ln=True)
        image_path = BASE_DIR / panel.image_url.lstrip("/")
        if image_path.exists():
            with Image.open(image_path) as img:
                w, h = img.size
            scale = min(180 / w, 115 / h)
            pdf.image(str(image_path), x=15, y=28, w=w * scale, h=h * scale)
        pdf.set_y(150)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 8, f"Panel {panel.panel_number}", ln=True)
        pdf.set_font("Helvetica", "", 10)
        for label, value in [("Scene", panel.scene), ("Narration", panel.narration), ("Caption", panel.caption), ("Dialogue", panel.dialogue)]:
            pdf.multi_cell(0, 6, f"{label}: {value}")
    filename = f"comic_{uuid4().hex[:10]}.pdf"
    pdf.output(str(EXPORT_DIR / filename))
    return "/static/exports/" + filename
