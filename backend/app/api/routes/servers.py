from fastapi import APIRouter, status, HTTPException
from typing import Any
from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError
from app.api.deps import SessionDep, CurrentUser
from app.models import ServerCreate, Server
from app import crud

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_server(session: SessionDep, current_user: CurrentUser, server_data: ServerCreate) -> Any:
    """
    Create a new server
    """
    try:
        server = crud.create_server(
            session=session, user_id=current_user.id, server_name=server_data.name)
        return server
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail="An unknown database error has occured, if this persists please contact support.")
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An error occured: {str(e)}") from e
