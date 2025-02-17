"""Translation Service.

This module provides the TranslationService class, which offers translation functionalities using a given Translator
instance. The TranslationService class includes methods to get the supported source and target languages, as well as to
translate text between languages.
"""

from core.translator import Translator


class TranslationService:
    """A service class that provides translation functionalities using a given Translator instance."""

    def __init__(self, translator: Translator) -> None:
        """Initialize the TranslationService with a Translator instance."""
        self.translator = translator

    def get_source_languages(self) -> list[str]:
        """Get the list of source languages supported by the translator."""
        return self.translator.get_source_languages()

    def get_target_languages(self) -> list[str]:
        """Get the list of target languages supported by the translator."""
        return self.translator.get_target_languages()

    def translate(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """Translate text from the source language to the target language."""
        return self.translator.translate(text, src_lang, tgt_lang)
