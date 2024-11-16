from fastapi import APIRouter

from app.api.routes import accounts

api_router = APIRouter()
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
