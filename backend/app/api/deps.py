from collections.abc import Generator
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session
from app.core.config import settings
from app.core.db import engine
from app.models import User, TokenData


def get_db() -> Generator[Session, None, None]:
    """
    Yields a database session.

    This function is a dependency that can be used in FastAPI routes to provide
    a database session.

    Yields:
        Generator[Session, None, None]: A generator that yields a database session.
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


# From fastapi.security oath2.py:
# The URL to obtain the OAuth2 token. This would be the *path operation*
# that has `OAuth2PasswordRequestForm` as a dependency.
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/accounts/login"
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    """
    Retrieve the current user based on the provided session and token.

    Args:
        session (SessionDep): The database session dependency.
        token (TokenDep): The token dependency containing the JWT.

    Returns:
        User: The user object corresponding to the token's subject.

    Raises:
        HTTPException: Error 403 if the token is invalid or the user is not found.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenData(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Authentication",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
