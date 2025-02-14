from unittest.mock import Mock

import lingua
import pytest
from lingua import Language

from core.detection import LanguageDetectionError, LanguageDetector

# Mocking the DetectionResult for testing purposes
class MockDetectionResult:
    def __init__(self, language, word_count):
        self.language = language
        self.word_count = word_count


@pytest.fixture
def supported_languages():
    return [Language.ENGLISH, Language.FRENCH, Language.GERMAN]


@pytest.fixture
def language_detector(supported_languages):
    detector = LanguageDetector(supported_languages)
    detector.detector = Mock(spec=lingua.LanguageDetector)
    detector.detector.detect_language_of.return_value = Language.ENGLISH
    detection_results = [
        MockDetectionResult(Language.ENGLISH, 5),
        MockDetectionResult(Language.FRENCH, 3),
    ]
    detector.detector.detect_multiple_languages_of.return_value = detection_results
    return detector


def test_language_detector_initialization(supported_languages):
    detector = LanguageDetector(supported_languages)
    assert detector.detector is not None


def test_language_detector_initialization_empty_languages():
    with pytest.raises(LanguageDetectionError):
        LanguageDetector([])


def test_detect_language(language_detector):
    text = "This is a test sentence."
    detected_language = language_detector.detect_language(text)
    assert detected_language == "en"


def test_detect_language_empty_text(language_detector):
    with pytest.raises(LanguageDetectionError):
        language_detector.detect_language("")


def test_detect_language_with_whitespace_text(language_detector):
    with pytest.raises(LanguageDetectionError):
        language_detector.detect_language("   ")


def test_detect_language_not_detected(language_detector):
    text = "This is a test sentence."
    language_detector.detector.detect_language_of = lambda _: None
    with pytest.raises(LanguageDetectionError):
        language_detector.detect_language(text)

def test_detect_language_with_non_ascii_characters(language_detector):
    text = "这是一个测试句子。"  # This is a test sentence in Chinese.
    language_detector.detector.detect_language_of.return_value = Language.CHINESE
    detected_language = language_detector.detect_language(text)
    assert detected_language == "zh"

def test_detect_language_with_mixed_languages(language_detector):
    text = "This is a test sentence. C'est une phrase de test."
    language_detector.detector.detect_language_of.return_value = Language.ENGLISH
    detected_language = language_detector.detect_language(text)
    assert detected_language == "en"

def test_detect_language_with_invalid_language_code(language_detector):
    text = "This is a test sentence."
    language_detector.detector.detect_language_of.return_value = None
    with pytest.raises(LanguageDetectionError):
        language_detector.detect_language(text)

def test_detect_multiple_languages(language_detector):
    text = "This is a test sentence."
    detected_languages = language_detector.detect_multiple_languages(text)
    assert "en" in detected_languages
    assert "fr" in detected_languages


def test_detect_multiple_languages_empty_text(language_detector):
    with pytest.raises(LanguageDetectionError):
        language_detector.detect_multiple_languages("")


def test_detect_multiple_languages_with_whitespace_text(language_detector):
    with pytest.raises(LanguageDetectionError):
        language_detector.detect_multiple_languages("   ")


def test_detect_multiple_languages_not_detected(language_detector):
    text = "This is a test sentence."
    language_detector.detector.detect_multiple_languages_of = lambda _: []
    with pytest.raises(LanguageDetectionError):
        language_detector.detect_multiple_languages(text)

def test_detect_multiple_languages_with_dominant_language(language_detector):
    text = "This is a test sentence. C'est une phrase de test. This is another test sentence."
    detection_results = [
        MockDetectionResult(Language.ENGLISH, 10),
        MockDetectionResult(Language.FRENCH, 3),
    ]
    language_detector.detector.detect_multiple_languages_of.return_value = detection_results
    detected_languages = language_detector.detect_multiple_languages(text)
    assert "en" in detected_languages
    assert "fr" in detected_languages

def test_detect_multiple_languages_with_equal_distribution(language_detector):
    text = "This is a test sentence. C'est une phrase de test."
    detection_results = [
        MockDetectionResult(Language.ENGLISH, 5),
        MockDetectionResult(Language.FRENCH, 5),
    ]
    language_detector.detector.detect_multiple_languages_of.return_value = detection_results
    detected_languages = language_detector.detect_multiple_languages(text)
    assert "en" in detected_languages
    assert "fr" in detected_languages

def test_detect_multiple_languages_with_large_text(language_detector):
    text = "This is a test sentence. " * 1000  # Large text input
    detection_results = [
        MockDetectionResult(Language.ENGLISH, 5000),
        MockDetectionResult(Language.FRENCH, 3000),
    ]
    language_detector.detector.detect_multiple_languages_of.return_value = detection_results
    detected_languages = language_detector.detect_multiple_languages(text)
    assert "en" in detected_languages
    assert "fr" in detected_languages

def test_calculate_word_counts(language_detector):
    detection_results = [
        MockDetectionResult(Language.ENGLISH, 5),
        MockDetectionResult(Language.FRENCH, 3),
    ]
    word_counts = language_detector._calculate_word_counts(detection_results)
    assert word_counts["en"] == 5
    assert word_counts["fr"] == 3


def test_select_languages(language_detector):
    language_word_counts = {"en": 5, "fr": 3, "de": 1}
    selected_languages = language_detector._select_languages(language_word_counts)
    assert selected_languages == []
