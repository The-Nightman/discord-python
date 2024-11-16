import pytest
from collections.abc import Generator
from fastapi.testclient import TestClient
from app.main import app
from app.core.logger import logger
from app.core.config import settings
from app.core.db import init_db
from app.models import User, Server, UserServerLink, Message
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
        yield session
        statement = delete(User)
        session.exec(statement)
        statement = delete(Server)
        session.exec(statement)
        statement = delete(UserServerLink)
        session.exec(statement)
        statement = delete(Message)
        session.exec(statement)
        session.commit()


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c