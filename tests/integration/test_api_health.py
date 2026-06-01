from fastapi.testclient import TestClient

from hokage_vision.api.app import create_app


def test_api_health() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_api_mock_image_detection() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/detect/image",
        json={"image_path": "examples/images/sample.jpg", "backend": "mock"},
    )

    assert response.status_code == 200
    assert response.json()["detections"][0]["label"] == "obito"
