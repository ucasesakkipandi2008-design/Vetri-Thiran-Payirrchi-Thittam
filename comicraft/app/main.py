from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.routes import router

BASE_DIR = Path(__file__).resolve().parent.parent
static_dir = BASE_DIR / "static"
(static_dir / "panels").mkdir(parents=True, exist_ok=True)
(static_dir / "exports").mkdir(parents=True, exist_ok=True)

app = FastAPI(title="ComicCraft", version="1.0.0")
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.include_router(router)
