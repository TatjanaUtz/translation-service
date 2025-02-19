"""Detector.

This module provides a class for detecting the language of a given text using the Lingua library.
"""

from lingua import Language, LanguageDetectorBuilder
from loguru import logger


class Detector:
    """A class used to detect the language of a given text."""

    def __init__(self, supported_languages: list[Language]) -> None:
        """Construct the language detector."""
        self.supported_languages = supported_languages
        self.detector = (
            LanguageDetectorBuilder.from_languages(*supported_languages).with_preloaded_language_models().build()
        )
        logger.debug("Language detector initialized with languages: {}", supported_languages)

    def detect_language(self, text: str) -> str:
        """Detect the language of the given text and return the ISO 639-1 code."""
        detected_language = self.detector.detect_language_of(text)
        return str(detected_language.iso_code_639_1.name.lower())
