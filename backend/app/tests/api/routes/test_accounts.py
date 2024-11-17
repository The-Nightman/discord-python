from fastapi.testclient import TestClient
from app.core.config import settings


def test_login_recieves_token(client: TestClient):
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    response = client.post(
        f"{settings.API_V1_STR}/accounts/login", data=login_data)
    token = response.json()
    assert response.status_code == 200
    assert "access_token" in token  # Check if the token key is present
    assert token["access_token"]  # Check if the token is not empty


def test_login_with_wrong_password(client: TestClient):
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": "wrong_password",
    }
    response = client.post(
        f"{settings.API_V1_STR}/accounts/login", data=login_data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}
    # Check if the token key is not present
    assert "access_token" not in response.json()


def test_register_new_user(client: TestClient):
    user_in = {
        "username": "testuser",
        "email": "testuser@mail.com",
        "password": "testpassword",
    }
    response = client.post(
        f"{settings.API_V1_STR}/accounts/register", json=user_in)
    token = response.json()
    assert response.status_code == 201
    assert "access_token" in token
    assert token["access_token"]


def test_register_used_email(client: TestClient):
    initial_user = {
        "username": "testuser",
        "email": "testuser@mail.com",
        "password": "testpassword",
    }
    user_in = {
        "username": "seconduser",
        "email": "testuser@mail.com",
        "password": "secrets!",
    }

    client.post(f"{settings.API_V1_STR}/accounts/register",
                json=initial_user)  # Register the initial user

    # Try to register the second user with the same email
    response = client.post(
        f"{settings.API_V1_STR}/accounts/register", json=user_in)

    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}
    # Check if the token key is not present
    assert "access_token" not in response.json()
