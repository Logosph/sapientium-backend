from fastapi.testclient import TestClient
from starlette import status


def test_healthcheck(client: TestClient) -> None:
    result = client.get("/health")

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == {"status": "ok"}
