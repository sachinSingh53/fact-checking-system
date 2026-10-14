from fastapi.testclient import TestClient


def test_root_describes_unimplemented_domain(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "fact-checking-system",
        "status": "ready-for-specification",
    }


def test_liveness_does_not_require_infrastructure(client: TestClient) -> None:
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
