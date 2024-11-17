from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import settings
from app.core import security
from app.api.deps import SessionDep
from app.models import Token, UserRegister
from app import crud

router = APIRouter()


@router.post("/login")
async def login(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """
    OAuth2 token login, get an access token for future requests
    """
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(session: SessionDep, form_data: UserRegister) -> Token:
    """
    Register a new user
    """
    # Check if the email is already registered
    user = crud.get_user_by_email(session=session, email=form_data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = crud.create_user(
        session=session, user_create=form_data
    )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
