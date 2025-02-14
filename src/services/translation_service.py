"""Translation Service.

This module provides a service for translating text using a specified translator.
"""

from core.translation import Translator


class TranslationService:
    """A service for translating text from one language to another."""

    def __init__(self, translator: Translator) -> None:
        """Initialize the TranslationService with a given translator."""
        self.translator = translator

    def translate(self, text: str, src_lang: str, tgt_lang: str, num_translations: int) -> list[str]:
        """Translate the given text from the source language to the target language.

        Args:
            text (str): The text to be translated.
            src_lang (str): The source language code.
            tgt_lang (str): The target language code.
            num_translations (int): The number of translations to perform.

        Returns:
            list[str]: A list of translated text strings.
        """
        return self.translator.translate(text, src_lang, tgt_lang, num_translations)
