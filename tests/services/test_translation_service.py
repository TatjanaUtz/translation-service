from unittest.mock import MagicMock

import pytest

from core.translation import Translator
from services.translation_service import TranslationService


@pytest.fixture
def mock_translator():
    return MagicMock(spec=Translator)


@pytest.fixture
def translation_service(mock_translator):
    return TranslationService(translator=mock_translator)


def test_translate_calls_translator(translation_service, mock_translator):
    text = "Hello"
    src_lang = "en"
    tgt_lang = "es"
    num_translations = 1

    translation_service.translate(text, src_lang, tgt_lang, num_translations)

    mock_translator.translate.assert_called_once_with(text, src_lang, tgt_lang, num_translations)


def test_translate_returns_correct_value(translation_service, mock_translator):
    text = "Hello"
    src_lang = "en"
    tgt_lang = "es"
    num_translations = 1
    expected_result = ["Hola"]

    mock_translator.translate.return_value = expected_result

    result = translation_service.translate(text, src_lang, tgt_lang, num_translations)

    assert result == expected_result
