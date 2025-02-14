"""Language Detection Module.

This module provides a class for detecting languages in text using the Lingua library. It supports detecting a single
language or multiple languages within a given text.
"""

from collections import defaultdict

import numpy as np
from lingua import DetectionResult, Language, LanguageDetectorBuilder
from loguru import logger


class LanguageDetectionError(Exception):
    """Custom exception for language detection errors."""


class LanguageDetector:
    """A class used to detect languages in text."""

    def __init__(self, supported_languages: list[Language]) -> None:
        """Initialize the LanguageDetector with the specified supported languages.

        Args:
            supported_languages (list[Language]): A list of supported languages.

        Raises:
            LanguageDetectionError: If the supported languages list is empty.
        """
        if not supported_languages:
            msg = "Supported languages list cannot be empty"
            logger.error(msg)
            raise LanguageDetectionError(msg)

        self.detector = (
            LanguageDetectorBuilder.from_languages(*supported_languages).with_preloaded_language_models().build()
        )
        logger.info("Language detector initialized with languages: {}", supported_languages)

    def detect_language(self, text: str) -> str:
        """Detect the language of the given text.

        Args:
            text (str): The text to detect the language of.

        Returns:
            str: The detected language code.

        Raises:
            LanguageDetectionError: If the text is empty or the language cannot be detected.
        """
        self._validate_text(text)
        detected_language = self.detector.detect_language_of(text)

        if not detected_language:
            msg = "Could not detect language"
            logger.error(msg)
            raise LanguageDetectionError(msg)

        logger.info(
            "Detected language: {} for text: {}",
            detected_language.iso_code_639_1.name.lower(),
            text,
        )
        return str(detected_language.iso_code_639_1.name.lower())

    def detect_multiple_languages(self, text: str) -> list[str]:
        """Detect multiple languages in the given text.

        Args:
            text (str): The text to detect the languages of.

        Returns:
            list[str]: A list of detected language codes.

        Raises:
            LanguageDetectionError: If the text is empty or no languages can be detected.
        """
        self._validate_text(text)
        detection_results = self.detector.detect_multiple_languages_of(text)

        if not detection_results:
            msg = "Could not detect any languages"
            logger.error(msg)
            raise LanguageDetectionError(msg)

        language_word_counts = self._calculate_word_counts(detection_results)
        selected_languages = self._select_languages(language_word_counts)

        if not selected_languages:
            logger.info("No languages outside 2 standard deviations - returning all languages")
            selected_languages = list({result.language.iso_code_639_1.name.lower() for result in detection_results})

        logger.info("Detected multiple languages: {}", selected_languages)
        return selected_languages

    def _validate_text(self, text: str) -> None:
        """Validate that the text is not empty.

        Args:
            text (str): The text to validate.

        Raises:
            LanguageDetectionError: If the text is empty.
        """
        if not text.strip():
            msg = "Text cannot be empty"
            logger.error(msg)
            raise LanguageDetectionError(msg)

    def _calculate_word_counts(self, detection_results: list[DetectionResult]) -> dict[str, int]:
        """Calculate the word counts for each detected language.

        Args:
            detection_results (list[DetectionResult]): The detection results.

        Returns:
            dict[str, int]: A dictionary with language codes as keys and word counts as values.
        """
        language_word_counts: dict[str, int] = defaultdict(int)
        for result in detection_results:
            language_word_counts[result.language.iso_code_639_1.name.lower()] += result.word_count
        return language_word_counts

    def _select_languages(self, language_word_counts: dict[str, int]) -> list[str]:
        """Select languages based on word counts using statistical thresholds.

        Args:
            language_word_counts (dict[str, int]): A dictionary with language codes as keys and word counts as values.

        Returns:
            list[str]: A list of selected language codes.
        """
        word_counts = list(language_word_counts.values())
        mean = np.mean(word_counts)
        std_dev = np.std(word_counts)
        return [
            lang
            for lang, count in language_word_counts.items()
            if count < (mean - 2 * std_dev) or count > (mean + 2 * std_dev)
        ]
