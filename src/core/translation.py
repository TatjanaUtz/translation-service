"""Translation Module.

This module provides a Translator class that can translate text between multiple languages using predefined translation
models.
"""

from itertools import product

from langcodes import Language
from loguru import logger
from transformers import pipeline


class TranslationError(Exception):
    """Exception raised for errors in the translation process."""


class TranslatorModel:
    """A class to handle text translation using a specific Helsinki-NLP model."""

    def __init__(self, source_language: str, target_language: str) -> None:
        """Initialize the TranslatorModel with the specified source and target language."""
        self.validate_language(source_language, "Source")
        self.validate_language(target_language, "Target")
        model_name = f"Helsinki-NLP/opus-mt-{source_language}-{target_language}"
        self.model = pipeline(task="translation", model=model_name)
        logger.info("Translator model initialized: {}", model_name)

    def translate(
        self,
        text: str,
        source_language: str | None = None,
        target_language: str | None = None,
        num_translations: int = 1,
    ) -> list[str]:
        """Translate the given text to the target language.

        Args:
            text (str): The text to translate.
            source_language (str, optional): The source language. Defaults to None.
            target_language (str, optional): The target language. Defaults to None.
            num_translations (int, optional): The number of translations to return. Defaults to 1.

        Returns:
            list[str]: A list of translated texts.

        Raises:
            TranslationError: If the text is empty, the number of translations is less than 1, or language validation
                              fails.
        """
        if not text.strip():
            msg = "Text to be translated cannot be empty"
            logger.error(msg)
            raise TranslationError(msg)

        if source_language:
            self.validate_language(source_language, "Source")

        if target_language:
            self.validate_language(target_language, "Target")

        if num_translations <= 0:
            msg = "Number of translations must be greater than 0"
            logger.error(msg)
            raise TranslationError(msg)

        outputs = self.model(
            text,
            src_lang=source_language,
            tgt_lang=target_language,
            clean_up_tokenization_spaces=True,
            num_beams=num_translations,
            num_return_sequences=num_translations,
        )
        return [output["translation_text"] for output in outputs]

    @staticmethod
    def validate_language(language: str, language_type: str) -> None:
        """Validate that the provided language is not empty."""
        if not language.strip():
            error_message = f"{language_type} language cannot be empty"
            logger.error(error_message)
            raise TranslationError(error_message)


class Translator:
    """A class used to translate text between multiple languages."""

    def __init__(self, source_languages: list[str], target_languages: list[str]) -> None:
        """Initialize the Translator with source and target languages."""
        self.validate_languages(source_languages, "Source")
        self.validate_languages(target_languages, "Target")
        self._create_translation_models(source_languages, target_languages)
        self.multi_language_to_english_model = TranslatorModel("mul", "en")
        self.english_to_multi_language_model = TranslatorModel("en", "mul")
        logger.info(
            "Translator initialized with source languages: {}, target languages: {}",
            source_languages,
            target_languages,
        )

    def _create_translation_models(self, source_languages: list[str], target_languages: list[str]) -> None:
        """Initialize translation models for each pair of source and target languages.

        This method creates a dictionary of translation models for each combination of source and target languages,
        excluding pairs where the source and target languages are the same. Each translation model is an instance of
        the `TranslatorModel` class. If an error occurs during the creation of a translation model, it is logged.

        Args:
            source_languages (list[str]): A list of source languages for which translation models need to be created.
            target_languages (list[str]): A list of target languages for which translation models need to be created.
        """
        self.models = {}
        for source_language, target_language in product(source_languages, target_languages):
            if source_language != target_language:
                try:
                    self.models[(source_language, target_language)] = TranslatorModel(source_language, target_language)
                except OSError as error:
                    logger.warning(
                        f"Could not create translation model for {source_language} to {target_language} -- ignoring it:"
                        f" {error}",
                    )

    def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
        num_translations: int,
    ) -> list[str]:
        """Translate the given text from the source language to the target language.

        Args:
            text (str): The text to be translated.
            source_language (str): The source language code.
            target_language (str): The target language code.
            num_translations (int): The number of translations to generate.

        Returns:
            list[str]: A list of translated texts.
        """
        self.validate_translation_params(text, source_language, target_language, num_translations)

        if source_language == target_language:
            logger.info("Text is already in the target language")
            translations = [text]
        elif (source_language, target_language) in self.models:
            translations = self._direct_translation(text, source_language, target_language, num_translations)
        elif source_language == "en":
            translations = self._english_to_multi_language_translation(text, target_language, num_translations)
        elif target_language == "en":
            translations = self._multi_language_to_english_translation(text, source_language, num_translations)
        else:
            translations = self._multi_step_translation(text, source_language, target_language, num_translations)

        logger.info("Generated translations: {} for text: {}", translations, text)
        return translations

    def _direct_translation(
        self,
        text: str,
        source_language: str,
        target_language: str,
        num_translations: int,
    ) -> list[str]:
        """Perform direct translation using the model for the given language pair."""
        logger.info("Using model for translation: {}", (source_language, target_language))
        model = self.models[(source_language, target_language)]
        return model.translate(text, num_translations=num_translations)

    def _english_to_multi_language_translation(
        self,
        text: str,
        target_language: str,
        num_translations: int,
    ) -> list[str]:
        """Translate text from English to the target language using the multi-language model."""
        logger.info("Using English to multi-language model for translation")
        language_code = Language.get(target_language).to_alpha3()
        preprocessed_text = f">>{language_code}<< {text}"
        return self.english_to_multi_language_model.translate(
            preprocessed_text,
            target_language=target_language,
            num_translations=num_translations,
        )

    def _multi_language_to_english_translation(
        self,
        text: str,
        source_language: str,
        num_translations: int,
    ) -> list[str]:
        """Translate text from the source language to English using the multi-language model."""
        logger.info("Using multi-language to English model for translation")
        return self.multi_language_to_english_model.translate(
            text,
            source_language=source_language,
            num_translations=num_translations,
        )

    def _multi_step_translation(
        self,
        text: str,
        source_language: str,
        target_language: str,
        num_translations: int,
    ) -> list[str]:
        """Translate text from the source language to the target language via English."""
        logger.info("Using multi-language to English and English to multi-language models for translation")
        english_translation = self.multi_language_to_english_model.translate(text, source_language=source_language)

        if not english_translation:
            msg = "Could not translate text to English"
            logger.error(msg)
            raise TranslationError(msg)

        language_code = Language.get(target_language).to_alpha3()
        preprocessed_text = f">>{language_code}<< {english_translation[0]}"
        return self.english_to_multi_language_model.translate(
            preprocessed_text,
            target_language=target_language,
            num_translations=num_translations,
        )

    @staticmethod
    def validate_languages(languages: list[str], language_type: str) -> None:
        """Validate the list of languages."""
        if not languages:
            error_message = f"{language_type} languages list cannot be empty"
            logger.error(error_message)
            raise TranslationError(error_message)

    @staticmethod
    def validate_translation_params(
        text: str,
        source_language: str,
        target_language: str,
        num_translations: int,
    ) -> None:
        """Validate the translation parameters."""
        if not text.strip():
            msg = "Text to be translated cannot be empty"
            logger.error(msg)
            raise TranslationError(msg)

        if not source_language.strip():
            msg = "Source language cannot be empty"
            logger.error(msg)
            raise TranslationError(msg)

        if not target_language.strip():
            msg = "Target language cannot be empty"
            logger.error(msg)
            raise TranslationError(msg)

        if num_translations <= 0:
            msg = "Number of translations must be greater than 0"
            logger.error(msg)
            raise TranslationError(msg)
