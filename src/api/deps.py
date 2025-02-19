"""Dependencies Module.

This file defines the dependencies for the API routes. It provides the language detection and the translation service.
"""

from fastapi import Request

from services.detection_service import DetectionService
from services.translation_service import TranslationService


def get_detection_service(request: Request) -> DetectionService:
    """Retrieve the language detection service from the application state."""
    return request.app.state.detection_service


def get_translation_service(request: Request) -> TranslationService:
    """Get the translation service from the application state."""
    return request.app.state.translation_service
