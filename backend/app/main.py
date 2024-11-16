from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.initial_data import main as db_init
from app.api.main import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup the database
    db_init()
    yield
    # After app has finished


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=None,
    lifespan=lifespan
)


@app.get("/", tags=["root"])
async def root():
    return {"message": "Hello World"}

app.include_router(api_router, prefix=settings.API_V1_STR)
