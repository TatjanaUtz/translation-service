"""Translation Endpoints.

This module defines the API endpoints for the translation service.
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.deps import get_language_detection_service, get_translation_service
from services.detection_service import LanguageDetectionService
from services.translation_service import TranslationService
from utils.language_utils import get_name_from_code

router = APIRouter()


class Language(BaseModel):
    """Represent a language with its code and name."""

    code: str
    name: str


@router.get("/translate/source-languages")  # type: ignore[misc]
async def get_source_languages(
    service: Annotated[TranslationService, Depends(get_translation_service)],
) -> list[Language]:
    """Endpoint to get the list of source languages supported by the translation service."""
    supported_languages = service.get_source_languages()
    language_names = [get_name_from_code(code) for code in supported_languages]
    return [Language(code=code, name=name) for code, name in zip(supported_languages, language_names, strict=False)]


@router.get("/translate/target-languages")  # type: ignore[misc]
async def get_target_languages(
    service: Annotated[TranslationService, Depends(get_translation_service)],
) -> list[Language]:
    """Endpoint to get the list of target languages supported by the translation service."""
    supported_languages = service.get_target_languages()
    language_names = [get_name_from_code(code) for code in supported_languages]
    return [Language(code=code, name=name) for code, name in zip(supported_languages, language_names, strict=False)]


class TranslationRequest(BaseModel):
    """Represent a translation request with the text to be translated and the source and target languages."""

    text: str
    source_language: str
    target_language: str


class TranslationResponse(BaseModel):
    """Represent a translation response with the detected language and the translated text."""

    detected_language: str | None
    translation: str


@router.post("/translate")  # type: ignore[misc]
async def translate_text(
    request: TranslationRequest,
    service: Annotated[TranslationService, Depends(get_translation_service)],
    detection_service: Annotated[LanguageDetectionService, Depends(get_language_detection_service)],
) -> TranslationResponse:
    """Endpoint to translate text from a source language to a target language."""
    if not request.source_language:
        detected_language = detection_service.detect_language(request.text)
        source_language = detected_language
    else:
        detected_language = None
        source_language = request.source_language
    translation = service.translate(request.text, source_language, request.target_language)
    return TranslationResponse(detected_language=detected_language, translation=translation)
