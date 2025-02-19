"""Detection Endpoints.

This module defines the API endpoint for the detection service.
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.deps import get_detection_service
from services.detection_service import DetectionService

router = APIRouter()


class DetectRequest(BaseModel):
    """Represent a request to detect the language of a given text."""

    text: str


class DetectResponse(BaseModel):
    """Response model for language detection endpoint."""

    detected_language: str


@router.post("/detect")  # type: ignore[misc]
async def detect_language(
    request: DetectRequest,
    service: Annotated[DetectionService, Depends(get_detection_service)],
) -> DetectResponse:
    """Detect the language of the given text."""
    detected_language = service.detect_language(request.text)
    return DetectResponse(detected_language=detected_language)
