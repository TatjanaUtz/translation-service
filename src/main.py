"""Main.

This module sets up and runs a FastAPI application for a translation service.

The application includes endpoints for language detection and translation,
and serves static files from the "frontend" directory.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from lingua import Language

from api.endpoints import detect, translate
from config import AppConfig
from core.detector import Detector
from core.translator import Translator
from services.detection_service import DetectionService
from services.translation_service import TranslationService

config = AppConfig()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    """Context manager for application lifespan events."""
    app.state.detection_service = DetectionService(Detector(Language.all()))
    app.state.translation_service = TranslationService(Translator(config.source_languages, config.target_languages))
    yield


app = FastAPI()  # lifespan=lifespan
app.include_router(detect.router, tags=["Language Detection"])
app.include_router(translate.router, tags=["Translation"])
app.mount(path="/", app=StaticFiles(directory="frontend", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # noqa: S104
