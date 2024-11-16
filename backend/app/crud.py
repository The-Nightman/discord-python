from sqlmodel import Session, select
from app.models import User, UserCreate
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