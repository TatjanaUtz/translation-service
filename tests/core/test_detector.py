from unittest.mock import MagicMock,patch

import pytest
from lingua import Language, LanguageDetector, LanguageDetectorBuilder

from core.detector import Detector


@pytest.fixture(autouse=True, name="mock_builder")
def mock_language_detector_builder():
    with patch("core.detector.LanguageDetectorBuilder", autospec=True) as mock:
        yield mock

@pytest.fixture(autouse=True)
def mock_detector(mock_builder):
    mocked_detector = MagicMock(LanguageDetector)
    mocked_builder = MagicMock(LanguageDetectorBuilder)
    mocked_builder.with_preloaded_language_models.return_value = mocked_builder
    mocked_builder.build.return_value = mocked_detector
    mock_builder.from_languages.return_value = mocked_builder
    return mocked_detector

@pytest.fixture
def supported_languages():
    return [Language.ENGLISH, Language.FRENCH, Language.GERMAN]

@pytest.fixture
def detector(supported_languages):
    return Detector(supported_languages)

def test_language_detector_initialization(supported_languages):
    detector = Detector(supported_languages)
    assert detector.detector is not None


def test_detect_language(detector):
    detector.detector.detect_language_of.return_value = Language.ENGLISH
    text = "This is a test sentence."
    detected_language = detector.detect_language(text)
    assert detected_language == "en"

def test_detect_language_with_non_ascii_characters(detector):
    text = "这是一个测试句子。"
    detector.detector.detect_language_of.return_value = Language.CHINESE
    detected_language = detector.detect_language(text)
    assert detected_language == "zh"

def test_detect_language_with_mixed_languages(detector):
    text = "This is a test sentence. C'est une phrase de test."
    detector.detector.detect_language_of.return_value = Language.ENGLISH
    detected_language = detector.detect_language(text)
    assert detected_language == "en"
