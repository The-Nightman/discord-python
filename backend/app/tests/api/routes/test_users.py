from fastapi.testclient import TestClient
from app.core.config import settings


def test_read_users_me(client: TestClient, normal_user_token_headers: dict[str, str]):
    response = client.get("/api/v1/users/my-profile",
                          headers=normal_user_token_headers)
    current_user = response.json()
    assert response.status_code == 200
    assert current_user["is_super_admin"] is False
    assert current_user["email"] == settings.TEST_USER
    assert current_user["username"] == settings.TEST_USER_USERNAME
