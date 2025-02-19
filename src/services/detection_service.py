"""Detection Service.

This module provides the DetectionService class for detecting the language of a given text.
"""

from core.detector import Detector


class DetectionService:
    """A service class for detecting the language of a given text using a specified detector."""

    def __init__(self, detector: Detector) -> None:
        """Initialize the DetectionService with a given detector."""
        self.detector = detector

    def detect_language(self, text: str) -> str:
        """Detect the language of the provided text."""
        return self.detector.detect_language(text)
