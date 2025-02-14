from unittest.mock import call, patch

import pytest

from core.translation import Translator, TranslatorModel, TranslationError


@pytest.fixture(autouse=True)
def mock_pipeline():
    with patch("core.translation.pipeline") as mock:
        yield mock


@pytest.fixture
def mock_logger():
    with patch("core.translation.logger") as mock:
        yield mock


@pytest.fixture
def translator_model():
    return TranslatorModel("en", "fr")


def test_translator_model_initialization(mock_pipeline, mock_logger):
    TranslatorModel("en", "fr")
    mock_pipeline.assert_called_once_with(task="translation", model="Helsinki-NLP/opus-mt-en-fr")
    mock_logger.info.assert_called_once_with("Translator model initialized: {}", "Helsinki-NLP/opus-mt-en-fr")


def test_translate_empty_text(translator_model):
    with pytest.raises(TranslationError) as excinfo:
        translator_model.translate("")
    assert "Text to be translated cannot be empty" in str(excinfo.value)


def test_translate_invalid_num_translations(translator_model):
    with pytest.raises(TranslationError) as excinfo:
        translator_model.translate("Hello", num_translations=0)
    assert "Number of translations must be greater than 0" in str(excinfo.value)


def test_translate_valid_input(translator_model):
    translator_model.model.return_value = [{"translation_text": "Bonjour"}]
    translations = translator_model.translate("Hello")
    assert translations == ["Bonjour"]


def test_validate_language_empty():
    with pytest.raises(TranslationError) as excinfo:
        TranslatorModel.validate_language("", "Source")
    assert "Source language cannot be empty" in str(excinfo.value)


def test_validate_language_valid():
    TranslatorModel.validate_language("en", "Source")



@pytest.fixture(autouse=True)
def mock_translator_model():
    with patch("core.translation.TranslatorModel", autospec=True) as mock:
        yield mock


@pytest.fixture
def translator_instance():
    source_languages = ["en", "es"]
    target_languages = ["fr", "de"]
    translator = Translator(source_languages, target_languages)
    return translator


def test_init_valid_languages(translator_instance):
    assert len(translator_instance.models) == 4  # 2 source languages * 2 target languages


def test_init_empty_source_languages():
    with pytest.raises(TranslationError) as excinfo:
        Translator([], ["en"])
    assert "Source languages list cannot be empty" in str(excinfo.value)


def test_init_empty_target_languages():
    with pytest.raises(TranslationError) as excinfo:
        Translator(["en"], [])
    assert "Target languages list cannot be empty" in str(excinfo.value)


def test_translate_empty_text(translator_instance):
    with pytest.raises(TranslationError) as excinfo:
        translator_instance.translate("", "en", "es", 1)
    assert "Text to be translated cannot be empty" in str(excinfo.value)


def test_translate_empty_source_language(translator_instance):
    with pytest.raises(TranslationError) as excinfo:
        translator_instance.translate("Hello", "", "es", 1)
    assert "Source language cannot be empty" in str(excinfo.value)


def test_translate_empty_target_language(translator_instance):
    with pytest.raises(TranslationError) as excinfo:
        translator_instance.translate("Hello", "en", "", 1)
    assert "Target language cannot be empty" in str(excinfo.value)


def test_translate_zero_translations(translator_instance):
    with pytest.raises(TranslationError) as excinfo:
        translator_instance.translate("Hello", "en", "es", 0)
    assert "Number of translations must be greater than 0" in str(excinfo.value)


def test_translate_same_language(translator_instance):
    translations = translator_instance.translate("Hello", "en", "en", 1)
    assert translations == ["Hello"]


def test_direct_translation(mock_translator_model, translator_instance):
    mock_translator_model.return_value.translate.return_value = ["Hallo"]
    translations = translator_instance.translate("Hello", "en", "de", 1)
    assert translations == ["Hallo"]
    mock_translator_model.return_value.translate.assert_called_once_with("Hello", num_translations=1)


def test_english_to_multi_language_translation(mock_translator_model, translator_instance):
    mock_translator_model.return_value.translate.return_value = ["Hola"]
    translations = translator_instance.translate("Hello", "en", "es", 1)
    assert translations == ["Hola"]
    mock_translator_model.return_value.translate.assert_called_once_with(
        ">>spa<< Hello", target_language="es", num_translations=1
    )


def test_multi_language_to_english_translation(mock_translator_model, translator_instance):
    mock_translator_model.return_value.translate.return_value = ["Hello"]
    translations = translator_instance.translate("Hola", "es", "en", 1)
    assert translations == ["Hello"]
    mock_translator_model.return_value.translate.assert_called_once_with(
        "Hola", source_language="es", num_translations=1
    )


def test_multi_step_translation(mock_translator_model, translator_instance):
    mock_translator_model.return_value.translate.side_effect = [["Hello"], ["Hallo"]]
    translations = translator_instance.translate("Bonjour", "fr", "de", 1)
    assert translations == ["Hallo"]
    assert mock_translator_model.return_value.translate.call_count == 2
    mock_translator_model.return_value.translate.assert_has_calls(
        [
            call("Bonjour", source_language="fr"),
            call(">>deu<< Hello", target_language="de", num_translations=1),
        ]
    )


def test_create_translation_models_success(mock_translator_model):
    source_languages = ["en", "fr"]
    target_languages = ["de", "es"]

    instance = Translator(source_languages, target_languages)

    expected_calls = [
        ("en", "de"),
        ("en", "es"),
        ("fr", "de"),
        ("fr", "es"),
        ("mul", "en"),
        ("en", "mul"),
    ]

    actual_calls = [call[0] for call in mock_translator_model.call_args_list]
    assert actual_calls == expected_calls
    assert len(instance.models) == 4


def test_create_translation_models_no_same_language_pairs(mock_translator_model):
    source_languages = ["en", "fr"]
    target_languages = ["en", "fr"]

    instance = Translator(source_languages, target_languages)

    expected_calls = [("en", "fr"), ("fr", "en"), ("mul", "en"), ("en", "mul")]

    actual_calls = [call[0] for call in mock_translator_model.call_args_list]
    assert actual_calls == expected_calls
    assert len(instance.models) == 2


def test_create_translation_models_error_handling(mock_translator_model):
    mock_translator_model.side_effect = [
        OSError("Mocked error"),
        mock_translator_model,
        mock_translator_model,
    ]
    source_languages = ["en"]
    target_languages = ["de"]

    with patch("core.translation.logger") as mock_logger:
        instance = Translator(source_languages, target_languages)

        mock_logger.warning.assert_called_once_with(
            "Could not create translation model for en to de -- ignoring it: Mocked error"
        )
        assert len(instance.models) == 0
