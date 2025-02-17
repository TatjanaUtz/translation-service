"""Translator.

This module provides a Translator class for translating text between multiple languages.
"""

from itertools import product

from langcodes import Language
from loguru import logger

from core.translator_model import TranslatorModel


class Translator:
    """Translator class for translating text between multiple languages."""

    def __init__(self, source_languages: list[str], target_languages: list[str]) -> None:
        """Initialize the Translator with source and target languages."""
        self.source_languages = source_languages
        self.target_languages = target_languages
        self._create_translation_models(source_languages, target_languages)
        self.multi_language_to_english_model = TranslatorModel("mul", "en")
        self.english_to_multi_language_model = TranslatorModel("en", "mul")

    def _create_translation_models(self, source_languages: list[str], target_languages: list[str]) -> None:
        """Create translation models for each source-target language pair."""
        self.models = {}
        for source_language, target_language in product(source_languages, target_languages):
            if source_language != target_language:
                try:
                    self.models[(source_language, target_language)] = TranslatorModel(source_language, target_language)
                except OSError:
                    logger.warning(
                        f"Could not create translation model for {source_language} to {target_language}",
                    )

    def get_source_languages(self) -> list[str]:
        """Get the list of source languages."""
        return self.source_languages

    def get_target_languages(self) -> list[str]:
        """Get the list of target languages."""
        return self.target_languages

    def translate(self, text: str, source_language: str, target_language: str) -> str:
        """Translate text from source language to target language."""
        self._validate_input(text, source_language, target_language)

        if source_language == target_language:
            logger.debug("Text is already in the target language")
            translation = text
        elif (source_language, target_language) in self.models:
            translation = self._direct_translation(text, source_language, target_language)
        elif source_language == "en":
            translation = self._english_to_multi_language_translation(text, target_language)
        elif target_language == "en":
            translation = self._multi_language_to_english_translation(text, source_language)
        else:
            translation = self._multi_step_translation(text, source_language, target_language)

        return translation

    def _validate_input(self, text: str, source_language: str, target_language: str) -> None:
        """Validate the input parameters for translation."""
        if not text.strip():
            msg = "Text to be translated cannot be empty"
            logger.error(msg)
            raise ValueError(msg)

        if not source_language.strip():
            msg = "Source language cannot be empty"
            logger.error(msg)
            raise ValueError(msg)

        if not target_language.strip():
            msg = "Target language cannot be empty"
            logger.error(msg)
            raise ValueError(msg)

    def _direct_translation(self, text: str, source_language: str, target_language: str) -> str:
        """Perform direct translation using the model."""
        logger.debug("Using model for translation: {}", (source_language, target_language))
        model = self.models[(source_language, target_language)]
        return model.translate(text)

    def _english_to_multi_language_translation(self, text: str, target_language: str) -> str:
        """Translate text from English to a target language."""
        logger.debug("Using English to multi-language model for translation")
        language_code = Language.get(target_language).to_alpha3()
        preprocessed_text = f">>{language_code}<< {text}"
        return self.english_to_multi_language_model.translate(preprocessed_text, target_language=target_language)

    def _multi_language_to_english_translation(self, text: str, source_language: str) -> str:
        """Translate text from a source language to English."""
        logger.debug("Using multi-language to English model for translation")
        return self.multi_language_to_english_model.translate(text, source_language=source_language)

    def _multi_step_translation(self, text: str, source_language: str, target_language: str) -> str:
        """Perform multi-step translation via English."""
        logger.debug("Using multi-language to English and English to multi-language models for translation")
        english_translation = self.multi_language_to_english_model.translate(text, source_language=source_language)

        if not english_translation:
            msg = "Could not translate text to English"
            logger.error(msg)
            raise ValueError(msg)

        language_code = Language.get(target_language).to_alpha3()
        preprocessed_text = f">>{language_code}<< {english_translation}"
        return self.english_to_multi_language_model.translate(preprocessed_text, target_language=target_language)
