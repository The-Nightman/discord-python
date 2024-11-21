from fastapi.testclient import TestClient
from sqlmodel import Session
from app import crud
from app.models import UserCreate
from app.core.config import settings


def inject_test_user(session: Session) -> None:
    """
    Injects a test user into the database session.

    Args:
        session (Session): The database session to use for injecting the test user.

    Returns:
        None
    """
    test_user_in = UserCreate(
        email=settings.TEST_USER,
        username=settings.TEST_USER_USERNAME,
        password=settings.TEST_USER_PASSWORD,
        is_super_admin=False,
    )
    crud.create_user(session=session, user_create=test_user_in)


def user_authentication_headers(*, client: TestClient, email: str, password: str) -> dict[str, str]:
    """
    Authenticate a user and return the authentication headers.
    Args:
        client (TestClient): The test client to use for making the request.
        email (str): The email of the user to authenticate.
        password (str): The password of the user to authenticate.
    Returns:
        dict[str, str]: A dictionary containing the authorization headers.
    """
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/accounts/login", data=data)
    response = r.json()
    token = response["access_token"]
    return {"Authorization": f"Bearer {token}"}


def super_admin_authentication_headers(*, client: TestClient) -> dict[str, str]:
    """
    Authenticate a super admin user and return the authentication headers.
    Args:
        client (TestClient): The test client to use for making the request.
    Returns:
        dict[str, str]: A dictionary containing the authorization headers.
    """
    admin_data = {"username": settings.FIRST_SUPERUSER,
                  "password": settings.FIRST_SUPERUSER_PASSWORD}

    r = client.post(f"{settings.API_V1_STR}/accounts/login", data=admin_data)
    response = r.json()
    token = response["access_token"]
    return {"Authorization": f"Bearer {token}"}
