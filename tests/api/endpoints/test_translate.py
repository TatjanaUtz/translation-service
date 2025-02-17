from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app

from api.deps import get_translation_service, get_language_detection_service
from services.translation_service import TranslationService
from services.detection_service import LanguageDetectionService

client = TestClient(app)

# Mock services
translation_service_mock = MagicMock(spec=TranslationService)
language_detection_service_mock = MagicMock(spec=LanguageDetectionService)

app.dependency_overrides[get_translation_service] = lambda: translation_service_mock
app.dependency_overrides[get_language_detection_service] = lambda: language_detection_service_mock


def test_get_source_languages():
    translation_service_mock.get_source_languages.return_value = ['en', 'es', 'fr']

    response = client.get("/translate/source-languages")

    assert response.status_code == 200
    assert response.json() == [
        {"code": "en", "name": "English"},
        {"code": "es", "name": "Spanish"},
        {"code": "fr", "name": "French"}
    ]

def test_get_target_languages():
    translation_service_mock.get_target_languages.return_value = ['de', 'it', 'ja']

    response = client.get("/translate/target-languages")

    assert response.status_code == 200
    assert response.json() == [
        {"code": "de", "name": "German"},
        {"code": "it", "name": "Italian"},
        {"code": "ja", "name": "Japanese"}
    ]

def test_translate_text_with_source_language():
    request_data = {
        "text": "Hello",
        "source_language": "en",
        "target_language": "es"
    }
    translation_service_mock.translate.return_value = "Hola"

    response = client.post("/translate", json=request_data)

    assert response.status_code == 200
    assert response.json() == {
        "detected_language": None,
        "translation": "Hola"
    }

def test_translate_text_without_source_language():
    request_data = {
        "text": "Bonjour",
        "source_language": "",
        "target_language": "en"
    }
    language_detection_service_mock.detect_language.return_value = "fr"
    translation_service_mock.translate.return_value = "Hello"

    response = client.post("/translate", json=request_data)

    assert response.status_code == 200
    assert response.json() == {
        "detected_language": "fr",
        "translation": "Hello"
    }
