from pathlib import Path
from uuid import uuid4
from PIL import Image, ImageDraw
from app.config import settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "static" / "panels"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def _placeholder(prompt: str, panel_number: int) -> Path:
    path = OUTPUT_DIR / f"panel_{panel_number}_{uuid4().hex[:8]}.png"
    image = Image.new("RGB", (settings.image_width, settings.image_height), "white")
    draw = ImageDraw.Draw(image)
    draw.text((30, 30), f"ComicCraft - Panel {panel_number}", fill="black")
    draw.text((30, 80), prompt[:180], fill="black")
    image.save(path)
    return path

def _local_image(prompt: str, panel_number: int) -> Path:
    from diffusers import StableDiffusionPipeline
    import torch
    pipe = StableDiffusionPipeline.from_pretrained(settings.local_image_model)
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    image = pipe(prompt, width=settings.image_width, height=settings.image_height, num_inference_steps=settings.image_steps, guidance_scale=settings.image_guidance).images[0]
    path = OUTPUT_DIR / f"panel_{panel_number}_{uuid4().hex[:8]}.png"
    image.save(path)
    return path

def _hf_image(prompt: str, panel_number: int) -> Path:
    from huggingface_hub import InferenceClient
    if not settings.hf_api_key:
        raise RuntimeError("HF_API_KEY is not configured.")
    client = InferenceClient(provider="hf-inference", api_key=settings.hf_api_key)
    image = client.text_to_image(prompt, model=settings.hf_image_model)
    path = OUTPUT_DIR / f"panel_{panel_number}_{uuid4().hex[:8]}.png"
    image.save(path)
    return path

def generate_image(prompt: str, panel_number: int) -> str:
    try:
        backend = settings.image_backend.lower().strip()
        if backend == "local":
            path = _local_image(prompt, panel_number)
        elif backend == "hf":
            path = _hf_image(prompt, panel_number)
        else:
            path = _placeholder(prompt, panel_number)
    except Exception:
        path = _placeholder(prompt, panel_number)
    return "/static/panels/" + path.name
