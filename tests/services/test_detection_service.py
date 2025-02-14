from unittest.mock import MagicMock

import pytest

from core.detection import LanguageDetector
from services.detection_service import LanguageDetectionService


@pytest.fixture
def mock_detector():
    return MagicMock(spec=LanguageDetector)


@pytest.fixture
def service(mock_detector):
    return LanguageDetectionService(detector=mock_detector)


def test_detect_language(service, mock_detector):
    text = "Hello, world!"
    mock_detector.detect_language.return_value = "en"

    result = service.detect_language(text)

    mock_detector.detect_language.assert_called_once_with(text)
    assert result == "en"


def test_detect_languages(service, mock_detector):
    text = "Hello, world! Bonjour le monde!"
    mock_detector.detect_multiple_languages.return_value = ["en", "fr"]

    result = service.detect_languages(text)

    mock_detector.detect_multiple_languages.assert_called_once_with(text)
    assert result == ["en", "fr"]
