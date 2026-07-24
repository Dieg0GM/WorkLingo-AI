from fastapi import FastAPI
from backend.models.request import TranslationRequest
from backend.services.translation_service import translate_text
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from backend.services.ai_router import ai_router

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "frontend"),
    name="static"
)


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "frontend" / "index.html")

@app.get("/about")
def about():
    return FileResponse(BASE_DIR / "frontend" / "about.html")


@app.post("/translate")
def translate(request: TranslationRequest):
    
    return ai_router(request)
