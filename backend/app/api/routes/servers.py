from fastapi import APIRouter, status, HTTPException
from typing import Any
from sqlalchemy.exc import SQLAlchemyError
from app.api.deps import SessionDep, CurrentUser
from app.models import ServerCreate, Server, ServerUpdate, ServerPublic
from app import crud

router = APIRouter()


@router.get("/{server_id}", response_model=ServerPublic, status_code=status.HTTP_200_OK)
async def get_server(session: SessionDep, current_user: CurrentUser, server_id: str) -> Any:
    """
    Get a server by ID
    """
    try:
        server = crud.get_server_by_id(session=session, server_id=server_id)
        if not server:
            raise HTTPException(
                status_code=404, detail="The server with this ID does not exist.")
        return server
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail="An unknown database error has occured, if this persists please contact support.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An error occured: {str(e)}") from e


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


@router.patch("/{server_id}/update", status_code=status.HTTP_200_OK)
async def update_server(session: SessionDep, current_user: CurrentUser, server_id: str, new_name: ServerUpdate) -> Any:
    """
    Update a server, limited to the server owner
    """
    try:
        if crud.user_is_owner(session=session, user_id=current_user.id, server_id=server_id) == False:
            raise HTTPException(
                status_code=403, detail="You do not have permission to update this server.")
        server = crud.update_server_name(
            session=session, server_id=server_id, name_in=new_name.name)
        if not server:
            raise HTTPException(
                status_code=404, detail="The server with this ID does not exist.")
        return server
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail="An unknown database error has occured, if this persists please contact support.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An error occured: {str(e)}") from e


@router.delete("/{server_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_server(session: SessionDep, current_user: CurrentUser, server_id: str) -> None:
    """
    Delete a server, limited to the server owner
    """
    try:
        if crud.user_is_owner(session=session, user_id=current_user.id, server_id=server_id) == False:
            raise HTTPException(
                status_code=403, detail="You do not have permission to delete this server.")
        crud.delete_server_by_id(session=session, server_id=server_id)
        return None
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail="An unknown database error has occured, if this persists please contact support.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An error occured: {str(e)}") from e
