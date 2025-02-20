"""Detector.

This module provides a class for detecting the language of a given text using the Lingua library.
"""

from lingua import Language, LanguageDetectorBuilder


class Detector:
    """A class used to detect the language of a given text."""

    def __init__(self, supported_languages: list[Language]) -> None:
        """Initializes the Detector with the given supported languages.

        Args:
            supported_languages (list[Language]): A list of supported Language objects.

        Raises:
            ValueError: If the supported_languages list is empty.
            DetectorInitializationError: If the language detector fails to initialize.
        """
        self.supported_languages = supported_languages
        self.detector = (
            LanguageDetectorBuilder.from_languages(*supported_languages).with_preloaded_language_models().build()
        )

    def detect_language(self, text: str) -> str:
        """Detects the language of the given text.

        Args:
            text (str): The text for which the language needs to be detected.

        Returns:
            str: The ISO 639-1 code of the detected language in lowercase.

        Raises:
            ValueError: If the input text is empty or contains only whitespace.
            DetectionError: If the language of the given text could not be detected.
        """
        detected_language = self.detector.detect_language_of(text)
        return str(detected_language.iso_code_639_1.name.lower())
