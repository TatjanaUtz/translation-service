"""Translator Model.

This module provides the TranslatorModel class, which handles translation tasks using the Hugging Face transformers
library.
"""

from loguru import logger
from transformers import pipeline


class TranslatorModel:
    """A class to handle translation tasks using the Hugging Face transformers library."""

    def __init__(self, source_language: str, target_language: str) -> None:
        """Initialize the TranslatorModel with the specified source and target languages."""
        model_name = f"Helsinki-NLP/opus-mt-{source_language}-{target_language}"
        self.model = pipeline(task="translation", model=model_name)
        logger.debug(f"Initialized translator model: {model_name}")

    def translate(self, text: str) -> str:
        """Translate the given text from the source language to the target language."""
        if not text.strip():
            msg = "Text to be translated cannot be empty"
            logger.error(msg)
            raise ValueError(msg)

        output = self.model(text, clean_up_tokenization_spaces=True)
        return output[0].get("translation_text")
