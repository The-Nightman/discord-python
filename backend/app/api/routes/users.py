from fastapi import APIRouter
from typing import Any
from app.api.deps import CurrentUser
from app.models import UserPublic

router = APIRouter()

@router.get("/my-profile", response_model=UserPublic)
async def read_users_me(*, current_user: CurrentUser) -> Any:
    return current_user