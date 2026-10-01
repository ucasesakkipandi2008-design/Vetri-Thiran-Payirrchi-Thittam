from pathlib import Path
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.models import PromptRequest, ComicResponse
from app.ai.gemini_flash import generate_outline
from app.ai.gemini_pro import generate_story
from app.ai.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / settings.templates_dir)
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"error": None})

async def _generate_comic(payload: PromptRequest) -> ComicResponse:
    outline = generate_outline(payload)
    story = generate_story(payload, outline)
    image_paths = [generate_image(p.image_prompt, p.panel_number) for p in outline.panels[:settings.max_panels]]
    panels = build_comic_layout(outline, story, image_paths)
    pdf_path = save_pdf(outline.title, panels)
    return ComicResponse(title=outline.title, panels=panels, pdf_path=pdf_path)

@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(request: Request, story_prompt: str = Form(...), character_name: str = Form("Alex"), setting: str = Form("A futuristic city"), tone: str = Form("Adventure"), art_style: str = Form("Comic book")):
    try:
        payload = PromptRequest(story_prompt=story_prompt, character_name=character_name, setting=setting, tone=tone, art_style=art_style)
        result = await _generate_comic(payload)
        return templates.TemplateResponse(request=request, name="comic_preview.html", context={"comic": result})
    except Exception as exc:
        return templates.TemplateResponse(request=request, name="error.html", context={"error": str(exc)}, status_code=500)

@router.post("/generate-comic/json")
async def generate_comic_json(payload: PromptRequest):
    return JSONResponse((await _generate_comic(payload)).model_dump())

@router.get("/test-image", response_class=HTMLResponse)
async def test_image(request: Request):
    try:
        image_path = generate_image("A friendly comic hero in a futuristic city, clean comic-book illustration", 999)
        return templates.TemplateResponse(request=request, name="image_test.html", context={"image_url": image_path})
    except Exception as exc:
        return templates.TemplateResponse(request=request, name="error.html", context={"error": str(exc)}, status_code=500)

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request):
    return templates.TemplateResponse(request=request, name="export_success.html", context={})
