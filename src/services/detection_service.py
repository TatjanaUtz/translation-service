"""Language Detection Service.

This module provides a service for detecting languages in text using a LanguageDetector.
"""

from core.detection import LanguageDetector


class LanguageDetectionService:
    """A service that uses a LanguageDetector to detect languages in text.

    Attributes:
        detector (LanguageDetector): An instance of LanguageDetector used for language detection.
    """

    def __init__(self, detector: LanguageDetector) -> None:
        """Initialize the LanguageDetectionService with a LanguageDetector."""
        self.detector = detector

    def detect_language(self, text: str) -> str:
        """Detect the language of the given text.

        Args:
            text (str): The text to detect the language of.

        Returns:
            str: The detected language.
        """
        return self.detector.detect_language(text)

    def detect_languages(self, text: str) -> list[str]:
        """Detect multiple languages in the given text.

        Args:
            text (str): The text to detect the languages of.

        Returns:
            list[str]: A list of detected languages.
        """
        return self.detector.detect_multiple_languages(text)
