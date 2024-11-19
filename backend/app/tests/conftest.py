import pytest
from collections.abc import Generator
from fastapi.testclient import TestClient
from app.main import app
from app.core.logger import logger
from app.core.config import settings
from app.core.db import init_db
from app.api.deps import get_db
from app.models import User, Server, UserServerLink, Message, Channel
from app.tests.utils.users import inject_test_user, user_authentication_headers
from sqlmodel import Session, create_engine, delete, SQLModel
from sqlalchemy_utils import database_exists, create_database

client = TestClient(app)

# Create a test database
test_engine = create_engine(str(settings.TEST_SQLALCHEMY_DATABASE_URI()))

# If test database does not exist, create it using and create all tables
if not database_exists(test_engine.url):
    logger.warning("Creating test database")
    create_database(test_engine.url)
    logger.info("Test database created")

# Place the table creation here incase something fails and it may not be caught by previous if statement
SQLModel.metadata.create_all(test_engine)
logger.info("Test database tables created")


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(test_engine) as session:
        init_db(session)
        inject_test_user(session)
        yield session
        statement = delete(UserServerLink)
        session.exec(statement)
        statement = delete(User)
        session.exec(statement)
        statement = delete(Channel)
        session.exec(statement)
        statement = delete(Server)
        session.exec(statement)
        statement = delete(Message)
        session.exec(statement)
        session.commit()


@pytest.fixture(scope="module")
def client(db: Session) -> Generator[TestClient, None, None]:

    # Override the testclient db dependency with the test db
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c

    # Clear the dependency overrides after the test is done
    app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient) -> dict[str, str]:
    return user_authentication_headers(client=client, email=settings.TEST_USER, password=settings.TEST_USER_PASSWORD)
