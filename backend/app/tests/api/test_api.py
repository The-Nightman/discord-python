from fastapi.testclient import TestClient
from sqlmodel import Session, select
from app.main import app
from app.core.config import settings
from app.models import User

client = TestClient(app)

# Test that pytest is working
def test_pytest_function():
    assert bool("true") == True


def test_api_is_live():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_initial_super_user_is_created(db: Session):
    # Query the database for the superuser
    user = db.exec(select(User).where(User.email == settings.FIRST_SUPERUSER)).first()

    # Check if the superuser exists
    assert user is not None
    assert user.email == settings.FIRST_SUPERUSER
    assert user.username == settings.FIRST_SUPERUSER_USERNAME
    assert user.is_super_admin == True