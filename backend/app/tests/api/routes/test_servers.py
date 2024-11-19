from fastapi.testclient import TestClient
from sqlmodel import Session, select
from app.core.config import settings
from app import crud
from app.models import Server, UserServerLink


def test_create_server(client: TestClient, normal_user_token_headers: dict[str, str], db: Session):
    owner_user = crud.get_user_by_email(session=db, email=settings.TEST_USER)
    response = client.post("/api/v1/servers/create", headers=normal_user_token_headers, json={"name": "test_server"})
    server_response = response.json()
    assert response.status_code == 201
    assert server_response["name"] == "test_server"
    assert server_response["id"] is not None

    # Check that the server was created in the database and the owner is a member
    server = db.exec(select(Server).where(Server.id == server_response["id"])).first()
    assert server is not None
    assert server.members[0].user_id == owner_user.id

    # Check that the owner has the owner role and is linked to the server
    user_link = db.exec(select(UserServerLink).where(UserServerLink.server_id == server.id and UserServerLink.user_id == owner_user.id)).first()
    assert user_link is not None
    assert user_link.user_id == owner_user.id
    assert user_link.server_id == server.id
    assert user_link.role == "owner"