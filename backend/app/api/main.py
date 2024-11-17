from fastapi import APIRouter

from app.api.routes import accounts, users

api_router = APIRouter()
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
