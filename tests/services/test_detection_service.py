from unittest.mock import patch

import pytest

from services.detection_service import DetectionService


@pytest.fixture(autouse=True)
def mock_detector():
    with patch("services.detection_service.Detector", autospec=True) as mock:
        yield mock

@pytest.fixture
def detection_service(mock_detector):
    return DetectionService(detector=mock_detector)


def test_detect_language(detection_service, mock_detector):
    text = "Hello, world!"
    mock_detector.detect_language.return_value = "en"
    result = detection_service.detect_language(text)
    mock_detector.detect_language.assert_called_once_with(text)
    assert result == "en"
