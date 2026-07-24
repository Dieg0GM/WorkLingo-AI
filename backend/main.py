from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.config.settings import settings
from backend.models.request import TranslationRequest
from backend.services.ai_router import ai_router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "frontend"),
    name="static",
)


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "frontend" / "index.html")


@app.get("/about")
def about():
    return FileResponse(BASE_DIR / "frontend" / "about.html")


@app.post("/translate")
async def translate(request: TranslationRequest):
    return await ai_router(request)
