import uuid
import random
import string
from sqlmodel import Session, select, delete
from app.models import User, UserCreate, Server, UserServerLink, Channel, ServerInviteCreate, ServerInvite
from app.core.security import get_password_hash, password_validation


def create_user(*, session: Session, user_create: UserCreate) -> User:
    """
    Create a new user in the database.

    Args:
        session (Session): The database session to use for the operation.
        user_create (UserCreate): An object containing the details of the user to be created.

    Returns:
        User: The newly created user object.
    """
    user = User.model_validate(user_create, update={
                               "hashed_password": get_password_hash(user_create.password)})
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate(*, session: Session, email: str, password: str) -> User:
    """
    Authenticate a user.

    Args:
        session (Session): The database session to use for the operation.
        email (str): The email of the user to authenticate.
        password (str): The password of the user to authenticate.

    Returns:
        User: The authenticated user.
    """
    user = session.exec(select(User).where(User.email == email)).first()
    # If the user does not exist or fails password check, return False
    if not user:
        return False
    if not password_validation(password, user.hashed_password):
        return False
    return user


def get_user_by_email(*, session: Session, email: str) -> User:
    """
    Get a user by email.

    Args:
        session (Session): The database session to use for the operation.
        email (str): The email of the user to retrieve.

    Returns:
        User: The user object.
    """
    user = session.exec(select(User).where(User.email == email)).first()
    return user


def get_server_by_id(*, session: Session, server_id: uuid.UUID) -> Server:
    """
    Get a server by ID.

    Args:
        session (Session): The database session to use for the operation.
        server_id (uuid.UUID): The UUID of the server to retrieve.

    Returns:
        Server: The server object.
    """
    server = session.exec(select(Server).where(Server.id == server_id)).first()
    return server


def create_server(*, session: Session, user_id: uuid.UUID, server_name: str) -> Server | Exception:
    """
    Create a new server with default channels and link the user as the owner.

    Args:
        session (Session): The database session to use for the transaction.
        user_id (uuid.UUID): The UUID of the user creating the server.
        server_name (str): The name of the server to be created.

    Returns:
        Server: The created Server object.

    Raises:
        Exception: If there is an error during the creation process, the transaction is rolled back and the exception is raised.
    """
    try:
        server = Server(name=server_name)
        session.add(server)
        session.flush()  # Flush to get the server ID but do not commit so we can rollback if needed

        # Create default channels, do it here instead of using a method so we can control the transaction
        text_channel = Channel(server_id=server.id,
                               name="General", type="text")
        session.add(text_channel)
        voice_channel = Channel(server_id=server.id,
                                name="General Voice", type="voice")
        session.add(voice_channel)

        # Link the user as the owner of the server
        user_server_link = UserServerLink(
            user_id=user_id, server_id=server.id, role="owner")
        session.add(user_server_link)

        # Commit the transaction, refresh the server object and return it
        session.commit()
        session.refresh(server)
        return server
    except Exception as e:
        # Rollback the transaction if an error occurs so nothing is saved to the database
        session.rollback()
        raise e


def user_is_owner(*, session: Session, user_id: uuid.UUID, server_id: uuid.UUID) -> bool:
    """
    Check if a user is the owner of a server.

    Args:
        session (Session): The database session to use for the operation.
        user_id (uuid.UUID): The UUID of the user to check.
        server_id (uuid.UUID): The UUID of the server to check.

    Returns:
        bool: True if the user is the owner of the server, False otherwise.
    """
    user_server_link = session.exec(select(UserServerLink).where(
        UserServerLink.user_id == user_id and UserServerLink.server_id == server_id)).first()

    if not user_server_link:
        return False

    return user_server_link.role == "owner"


def update_server_name(*, session: Session, server_id: Server, name_in: str) -> Server | None:
    """
    Update the name of a server in the database.

    Args:
        session (Session): The database session to use for the update.
        server_id (Server): The ID of the server to update.
        name_in (str): The new name to assign to the server.

    Returns:
        Server | None: The updated server object if the update was successful, otherwise None.
    """
    server = session.get(Server, server_id)
    server.name = name_in
    session.add(server)
    session.commit()
    session.refresh(server)
    return server


def create_invite(*, session: Session, creator_id: uuid.UUID, invite_data: ServerInviteCreate) -> ServerInvite:
    """
    Create an invite for a server.

    Args:
        session (Session): The database session to use for the operation.
        creator_id (uuid.UUID): The UUID of the user creating the invite.
        invite_data (ServerInviteCreate): An object containing the details of the invite to be created.

    Returns:
        str: The invite code.
    """
    invite = ServerInvite.model_validate(invite_data,
                                         update={
                                             "creator_id": creator_id,
                                         })
    session.add(invite)
    session.commit()
    session.refresh(invite)
    return invite


def delete_server_by_id(*, session: Session, server_id: uuid.UUID) -> None:
    """
    Delete a server by ID.

    Args:
        session (Session): The database session to use for the operation.
        server_id (uuid.UUID): The UUID of the server to delete.
    """
    try:
        # Use begin_nested() to run the transaction, begin() does not work in a try catch block
        # See examples here: https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#using-savepoint
        with session.begin_nested():
            session.exec(delete(UserServerLink).where(
                UserServerLink.server_id == server_id))
            session.exec(delete(Channel).where(Channel.server_id == server_id))
            session.exec(delete(ServerInvite).where(
                ServerInvite.server_id == server_id))
            # Messages are deleted via cascade
            server = session.get(Server, server_id)
            session.delete(server)
        session.commit()
        return None
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
