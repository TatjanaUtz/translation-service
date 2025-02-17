from unittest.mock import MagicMock, patch

import pytest

from core.translator import Translator
from services.translation_service import TranslationService


@pytest.fixture(autouse=True)
def mock_translator():
    with patch("services.translation_service.Translator", autospec=True) as mock:
        yield mock

@pytest.fixture
def translation_service(mock_translator):
    return TranslationService(translator=mock_translator)

def test_get_source_languages(mock_translator, translation_service):
    source_languages = ['en', 'de', 'fr']
    mock_translator.get_source_languages.return_value = source_languages
    assert translation_service.get_source_languages() == source_languages
    mock_translator.get_source_languages.assert_called_once()

def test_get_target_languages(mock_translator, translation_service):
    target_languages = ['en', 'de', 'fr']
    mock_translator.get_target_languages.return_value = target_languages
    assert translation_service.get_target_languages() == target_languages
    mock_translator.get_target_languages.assert_called_once()

def test_translate_basic(mock_translator, translation_service):
    translation = "Hello translated from en to de"
    mock_translator.translate.return_value = translation
    result = translation_service.translate("Hello", "en", "de")
    assert result == translation
    mock_translator.translate.assert_called_once_with("Hello", "en", "de")
