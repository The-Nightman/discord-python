from fastapi.testclient import TestClient
from sqlmodel import Session
from app.core.config import settings


def test_login_recieves_token(client: TestClient, db: Session):
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    response = client.post("/api/v1/accounts/login", data=login_data)
    token = response.json()
    assert response.status_code == 200
    assert "access_token" in token # Check if the token key is present
    assert token["access_token"] # Check if the token is not empty


def test_login_with_wrong_password(client: TestClient):
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": "wrong_password",
    }
    response = client.post("/api/v1/accounts/login", data=login_data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}
    assert "access_token" not in response.json() # Check if the token key is not present