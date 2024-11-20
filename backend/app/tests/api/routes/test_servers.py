from fastapi.testclient import TestClient
from sqlmodel import Session, select
from app.core.config import settings
from app import crud
from app.models import Server, UserServerLink, ServerInvite, User
from app.tests.utils import utils
import re


def test_create_server(client: TestClient, normal_user_token_headers: dict[str, str], db: Session):
    owner_user = crud.get_user_by_email(session=db, email=settings.TEST_USER)
    response = client.post("/api/v1/servers/create",
                           headers=normal_user_token_headers, json={"name": "test_server"})
    server_response = response.json()
    assert response.status_code == 201
    assert server_response["name"] == "test_server"
    assert server_response["id"] is not None

    # Check that the server was created in the database and the owner is a member
    server = db.exec(select(Server).where(
        Server.id == server_response["id"])).first()
    assert server is not None
    assert server.members[0].user_id == owner_user.id

    # Check that the owner has the owner role and is linked to the server
    user_link = db.exec(select(UserServerLink).where(UserServerLink.server_id == server.id).where(
        UserServerLink.user_id == owner_user.id)).first()
    assert user_link is not None
    assert user_link.user_id == owner_user.id
    assert user_link.server_id == server.id
    assert user_link.role == "owner"


def test_get_server_by_id(client: TestClient, normal_user_token_headers: dict[str, str], db: Session):
    server = db.exec(select(Server)).first()
    response = client.get(
        f"/api/v1/servers/{server.id}", headers=normal_user_token_headers)
    server_response = response.json()
    assert response.status_code == 200
    assert server_response["name"] == server.name
    assert server_response["id"] == str(server.id)
    assert "channels" in server_response
    assert "members" in server_response


def test_rename_server(client: TestClient, normal_user_token_headers: dict[str, str], db: Session):
    # Currently reads the server created in the previous test, fails if run alone, will be refactored later
    server = db.exec(select(Server)).first()
    response = client.patch(f"/api/v1/servers/{server.id}/update",
                            headers=normal_user_token_headers, json={"name": "new_name"})
    server_response = response.json()
    assert response.status_code == 200
    assert server_response["name"] == "new_name"
    assert server_response["id"] == str(server.id)

    # Check that the server was updated in the database
    updated_server = db.exec(select(Server).where(
        Server.id == server.id)).first()
    assert updated_server is not None
    assert updated_server.name == "new_name"
    assert updated_server.id == server.id


def test_create_invite(client: TestClient, normal_user_token_headers: dict[str, str], db: Session):
    server = db.exec(select(Server)).first()
    invite_data = {"server_id": str(server.id), "invite_code": utils.random_lower_string(8),
                   "expires_at": 0, "uses": 5}
    response = client.post(
        f"/api/v1/servers/{server.id}/invite", headers=normal_user_token_headers, json=invite_data)
    invite_response = response.json()
    assert response.status_code == 201
    assert "invite_code" in invite_response

    # Use regex to capture an 8-character string and a UUID4
    match = re.match(
        r"invite::(?P<invite_code>[a-zA-Z0-9]{8}):(?P<server_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})", invite_response["invite_code"])
    assert match is not None

    # Check that the invite code and server ID portions of the invite string match the data sent
    invite_code = match.group("invite_code")
    server_id = match.group("server_id")
    assert invite_code == invite_data["invite_code"]
    assert server_id == str(server.id)

    # Check that the invite was created in the database
    invite = db.exec(select(ServerInvite).where(
        ServerInvite.invite_code == invite_code)).first()
    assert invite is not None
    assert invite.server_id == server.id


def test_join_server(client: TestClient, super_admin_token_headers: dict[str, str], db: Session):
    user = crud.get_user_by_email(session=db, email=settings.FIRST_SUPERUSER)
    server = db.exec(select(Server)).first()
    invite = db.exec(select(ServerInvite).where(ServerInvite.server_id == server.id)).first()
    response = client.post(
        f"/api/v1/servers/{server.id}/join/?invite_code={invite.invite_code}", headers=super_admin_token_headers)

    assert response.status_code == 204
    # Check that the user was added to the server in the database

    membership = db.exec(select(UserServerLink).where(
        UserServerLink.server_id == server.id).where(UserServerLink.user_id == user.id)).first()

    assert membership is not None
    assert membership.server_id == server.id

    # This is failing as for some reason the user added in the user register test is being passed through the endpoint no matter what
    assert membership.user_id == user.id
    assert membership.role == "member"


def test_leave_server(client: TestClient, super_admin_token_headers: dict[str, str], db: Session):
    user = crud.get_user_by_email(session=db, email=settings.FIRST_SUPERUSER)
    server = db.exec(select(Server)).first()
    response = client.delete(
        f"/api/v1/servers/{server.id}/leave", headers=super_admin_token_headers)
    assert response.status_code == 204

    # Check that the user was removed from the server in the database
    membership = db.exec(select(UserServerLink).where(
        UserServerLink.server_id == server.id).where(UserServerLink.user_id == user.id)).first()
    assert membership is None


def test_delete_server(client: TestClient, normal_user_token_headers: dict[str, str], db: Session):
    server = db.exec(select(Server)).first()
    response = client.delete(
        f"/api/v1/servers/{server.id}/delete", headers=normal_user_token_headers)
    assert response.status_code == 204

    # Check that the server was deleted from the database
    deleted_server = db.exec(select(Server).where(
        Server.id == server.id)).first()
    assert deleted_server is None
    user_link = db.exec(select(UserServerLink).where(
        UserServerLink.server_id == server.id)).all()
    assert len(user_link) == 0
