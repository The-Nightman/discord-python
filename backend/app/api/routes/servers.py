from fastapi import APIRouter, status, HTTPException, Query
from typing import Any, Annotated
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from app.api.deps import SessionDep, CurrentUser
from app.models import ServerCreate, ServerInviteCreate, ServerUpdate, ServerPublic
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


@router.post("/{server_id}/invite", status_code=status.HTTP_201_CREATED)
async def create_invite(session: SessionDep, current_user: CurrentUser, invite_data: ServerInviteCreate) -> dict[str, str]:
    """
    Create an invite for a server
    """
    try:
        invite = crud.create_invite(
            session=session, creator_id=current_user.id, invite_data=invite_data)
        return {"invite_code": f"invite::{invite.invite_code}:{invite.server_id}"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail="An unknown database error has occured, if this persists please contact support.")
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An error occured: {str(e)}") from e


class InviteParams(BaseModel):
    invite_code: str


@router.post("/{server_id}/join/", status_code=status.HTTP_204_NO_CONTENT)
async def join_server(session: SessionDep, current_user: CurrentUser, server_id: str, filter_query: Annotated[InviteParams, Query()]) -> None:
    """
    Join a server using an invite code
    """
    try:
        invite_code = filter_query.invite_code
        crud.join_server_by_invite_code(
            session=session, user_id_in=current_user.id, server_id=server_id, invite_code=invite_code)
        return None
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail="An unknown database error has occured, if this persists please contact support.")
    except HTTPException as e:
        raise e
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


class ServerUserPromote(BaseModel):
    user_id: str
    new_role: str


@router.patch("/{server_id}/promote-user", status_code=status.HTTP_204_NO_CONTENT)
async def update_role(session: SessionDep, current_user: CurrentUser, server_id: str, promotion_data: ServerUserPromote) -> None:
    """
    Update a user's role in a server, limited to the server owner
    """
    try:
        crud.update_user_role(
            session=session, server_id=server_id, admin_user_id=current_user.id, update_user_id=promotion_data.user_id, new_role=promotion_data.new_role)
        return None
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


@router.delete("/{server_id}/leave", status_code=status.HTTP_204_NO_CONTENT)
async def leave_server(session: SessionDep, current_user: CurrentUser, server_id: str) -> None:
    """
    Leave a server
    """
    try:
        if crud.user_is_owner(session=session, user_id=current_user.id, server_id=server_id):
            raise HTTPException(
                status_code=403, detail="You cannot leave a server that you own.")
        crud.remove_user_from_server(
            session=session, user_id=current_user.id, server_id=server_id)
        return None
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail="An unknown database error has occured, if this persists please contact support.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"An error occured: {str(e)}") from e
