import pytest
from unittest.mock import MagicMock, patch
from core.translator import Translator
from core.translator_model import TranslatorModel

@pytest.fixture(autouse=True)
def mock_translator_model():
    with patch("core.translator.TranslatorModel", autospec=True) as mock:
        yield mock

@pytest.fixture(autouse=True)
def mock_translate(mock_translator_model):
    mock_model = MagicMock(TranslatorModel)
    mock_translator_model.return_value = mock_model
    yield mock_model.translate

@pytest.fixture
def translator():
    source_languages = ["en", "fr", "de"]
    target_languages = ["en", "fr", "de"]
    return Translator(source_languages, target_languages)

def test_initialization(translator):
    assert len(translator.models) == 6

def test_get_source_languages(translator):
    assert translator.get_source_languages() == ["en", "fr", "de"]

def test_get_target_languages(translator):
    assert translator.get_target_languages() == ["en", "fr", "de"]

def test_translate_empty_text(translator):
    with pytest.raises(ValueError, match="Text to be translated cannot be empty"):
        translator.translate("", "en", "fr")

def test_translate_empty_source_language(translator):
    with pytest.raises(ValueError, match="Source language cannot be empty"):
        translator.translate("Hello", "", "fr")

def test_translate_empty_target_language(translator):
    with pytest.raises(ValueError, match="Target language cannot be empty"):
        translator.translate("Hello", "en", "")

def test_translate_same_source_target_language(translator):
    text = "Hello"
    assert translator.translate(text, "en", "en") == text

def test_direct_translation(mock_translate, translator):
    mock_translate.return_value = "Bonjour"
    text = "Hello"
    result = translator.translate(text, "en", "fr")
    assert result == "Bonjour"
    mock_translate.assert_called_once_with(text)

def test_english_to_multi_language_translation(mock_translate, translator):
    mock_translate.return_value = "Hola"
    text = "Hello"
    result = translator.translate(text, "en", "es")
    assert result == "Hola"
    mock_translate.assert_called_once_with(">>spa<< Hello", target_language="es")

def test_multi_language_to_english_translation(mock_translate, translator):
    mock_translate.return_value = "Hello"
    text = "Hola"
    result = translator.translate(text, "es", "en")
    assert result == "Hello"
    mock_translate.assert_called_once_with(text, source_language="es")

def test_multi_step_translation(mock_translate, translator):
    mock_translate.side_effect = ["Hello", "Hola"]
    text = "Hallo"
    result = translator.translate(text, "de", "es")
    assert result == "Hola"
    assert mock_translate.call_count == 2
    mock_translate.assert_any_call(text, source_language="de")
    mock_translate.assert_any_call(">>spa<< Hello", target_language="es")

def test_create_translation_models(translator):
    assert ("en", "fr") in translator.models
    assert ("fr", "en") in translator.models
    assert ("de", "fr") in translator.models

def test_create_translation_models_oserror(mock_translator_model):
    mock_translator_model.side_effect = [OSError(), MagicMock(), MagicMock()]
    source_languages = ["en"]
    target_languages = ["fr"]
    translator = Translator(source_languages, target_languages)
    assert ("en", "fr") not in translator.models
