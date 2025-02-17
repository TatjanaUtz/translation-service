import pytest
from unittest.mock import patch, MagicMock

from core.translator_model import TranslatorModel


# Test Initialization
def test_initialization_success():
    with patch('core.translator_model.pipeline') as mock_pipeline:
        mock_pipeline.return_value = MagicMock()
        translator = TranslatorModel("en", "de")
        assert translator.model is not None

# Test Translation
def test_translation_success():
    with patch('core.translator_model.pipeline') as mock_pipeline:
        mock_pipeline.return_value = MagicMock(return_value=[{"translation_text": "Hallo, Welt!"}])
        translator = TranslatorModel("en", "de")
        result = translator.translate("Hello, world!")
        assert result == "Hallo, Welt!"

def test_translation_empty_string():
    translator = TranslatorModel("en", "de")
    with pytest.raises(ValueError, match="Text to be translated cannot be empty"):
        translator.translate("")

def test_translation_special_characters():
    with patch('core.translator_model.pipeline') as mock_pipeline:
        mock_pipeline.return_value = MagicMock(return_value=[{"translation_text": "Hallo, @Welt!"}])
        translator = TranslatorModel("en", "de")
        result = translator.translate("Hello, @world!")
        assert result == "Hallo, @Welt!"

def test_translation_long_string():
    long_text = "Hello, world! " * 1000  # Very long string
    with patch('core.translator_model.pipeline') as mock_pipeline:
        mock_pipeline.return_value = MagicMock(return_value=[{"translation_text": "Hallo, Welt! " * 1000}])
        translator = TranslatorModel("en", "de")
        result = translator.translate(long_text)
        assert result == "Hallo, Welt! " * 1000
