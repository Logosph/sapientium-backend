from fastapi.testclient import TestClient
from starlette import status


def test_healthcheck(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
