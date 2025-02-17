import pytest
from unittest.mock import patch, MagicMock

from core.translator_model import TranslatorModel

@pytest.fixture(autouse=True)
def mock_pipeline():
    with patch("core.translator_model.pipeline") as mock:
        yield mock

def test_initialization(mock_pipeline):
    mock_pipeline.return_value = MagicMock()
    translator = TranslatorModel("en", "de")
    assert translator.model is not None
    mock_pipeline.assert_called_once_with(task="translation", model="Helsinki-NLP/opus-mt-en-de")


def test_translate_success(mock_pipeline):
    mock_pipeline.return_value = MagicMock(return_value=[{"translation_text": "Hallo, Welt!"}])
    translator = TranslatorModel("en", "de")
    result = translator.translate("Hello, world!")
    assert result == "Hallo, Welt!"

def test_translate_empty_string():
    translator = TranslatorModel("en", "de")
    with pytest.raises(ValueError, match="Text to be translated cannot be empty"):
        translator.translate("")

def test_translate_special_characters(mock_pipeline):
    mock_pipeline.return_value = MagicMock(return_value=[{"translation_text": "Hallo, @Welt!"}])
    translator = TranslatorModel("en", "de")
    result = translator.translate("Hello, @world!")
    assert result == "Hallo, @Welt!"

def test_translate_long_string(mock_pipeline):
    long_text = "Hello, world! " * 1000  # Very long string
    mock_pipeline.return_value = MagicMock(return_value=[{"translation_text": "Hallo, Welt! " * 1000}])
    translator = TranslatorModel("en", "de")
    result = translator.translate(long_text)
    assert result == "Hallo, Welt! " * 1000

def test_translate_src_tgt_language_parameters(mock_pipeline):
    mock_model = MagicMock()
    mock_pipeline.return_value = mock_model
    translator = TranslatorModel("en", "de")
    translator.translate("Hello, world!", "en", "de")
    mock_model.assert_called_with("Hello, world!", src_lang="en", tgt_lang="de", clean_up_tokenization_spaces=True)
