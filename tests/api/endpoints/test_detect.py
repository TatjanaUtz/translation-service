from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from api.deps import get_detection_service
from main import app
from services.detection_service import DetectionService


client = TestClient(app)
detection_service_mock = MagicMock(spec=DetectionService)
app.dependency_overrides[get_detection_service] = lambda: detection_service_mock


def test_detect_language():
    request_data = {"text": "Hello world!"}
    detection_service_mock.detect_language.return_value = "en"

    response = client.post("/detect", json=request_data)

    assert response.status_code == 200
    assert response.json() == {"detected_language": "en"}
