import bcrypt
import jwt
from typing import Any
from datetime import datetime, timedelta, timezone
from app.core.config import settings


def get_password_hash(password: str) -> str:
    """
    Hashes a password using bcrypt.

    Remarks:
        passlib has not been maintained since 2020 and so despite having a module used
        in conjunction with bcrypt and its algorithms, it is not recommended to use it.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return bcrypt.hashpw(
        bytes(password, encoding="utf-8"),
        bcrypt.gensalt(),
    )


def create_access_token(data: str | Any, expires_delta: timedelta):
    """
    Creates a JSON Web Token (JWT) for the given data with an expiration time.

    Args:
        data (str | Any): The user identifier to be encoded in the token.
        expires_delta (timedelta): The time duration after which the token will expire.
            This is set in .env as ACCESS_TOKEN_EXPIRE_MINUTES or is 12 hours by default.

    Returns:
        str: The encoded JWT as a string.
    """
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = ({"exp": expire, "sub": str(data)})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def password_validation(plain_password: str, hashed_password: str) -> bool:
    """
    Validate a plain text password against a hashed password using bcrypt.

    Args:
        plain_password (str): The plain text password to validate.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain text password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(
        bytes(plain_password, encoding="utf-8"),
        bytes(hashed_password, encoding="utf-8"),
    )