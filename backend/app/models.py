import uuid
from enum import Enum as PyEnum
from sqlalchemy import Index, Enum as SQLAEnum
from datetime import datetime, timezone
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship, Column


# Shared properties
class UserBase(SQLModel):
    username: str = Field(max_length=100,index=True, nullable=False)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_super_admin: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=255)


class UserRegister(SQLModel):
    username: str
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=255)


# Properties to receive via API on update
class UserUpdate(UserBase):
    username: str | None
    email: EmailStr | None = Field(default="none", max_length=255)
    password: str | None = Field(min_length=8, max_length=255)


# Properties to return to client
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False)
    servers: list["UserServerLink"] = Relationship(back_populates="user")


class UserPublic(UserBase):
    id: uuid.UUID


# Shared properties
class ServerBase(SQLModel):
    name: str = Field(max_length=100, nullable=False)


# Properties to receive via API on creation
class ServerCreate(ServerBase):
    pass


# Properties to receive via API on update
class ServerUpdate(ServerBase):
    name: str | None = Field(max_length=100)


# Properties to return to client
class Server(ServerBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    channels: list["Channel"] = Relationship(back_populates="server")
    members: list["UserServerLink"] = Relationship(back_populates="server")


class ServerPublic(ServerBase):
    id: uuid.UUID
    name: str
    channels: list["Channel"]
    members: list["UserServerLink"]


# Define the accepted user roles
class UserRole(str, PyEnum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


# Intermediary table for user-server relationships and metadata
class UserServerLink(SQLModel, table=True):
    user_id: uuid.UUID = Field(foreign_key="user.id", primary_key=True)
    server_id: uuid.UUID = Field(foreign_key="server.id", primary_key=True)

    # User's role in the server
    role: UserRole = Field(sa_column=Column(SQLAEnum(UserRole), default=UserRole.MEMBER, nullable=False))

    # User's join date
    joined_at: int = Field(default_factory=lambda: int(datetime.now(timezone.utc).timestamp()), nullable=False)
    
    user: User = Relationship(back_populates="servers")
    server: Server = Relationship(back_populates="members")

    # Ensure that each server has only one owner
    __table_args__ = (
        Index(
            'unique_server_owner', # Index name
            'server_id', # Column to index
            unique=True, # Ensure uniqueness
            postgresql_where=(role == UserRole.OWNER)), # Only index rows where the user is an owner
    )


# Define the accepted channel types
class ChannelType(str, PyEnum):
    TEXT = "text"
    VOICE = "voice"


# Shared properties
class ChannelBase(SQLModel):
    name: str = Field(max_length=100, nullable=False)
    type: ChannelType = Field(sa_column=Column(SQLAEnum(ChannelType), nullable=False))


# Properties to receive via API on creation
class ChannelCreate(ChannelBase):
    pass


# Properties to receive via API on update
class ChannelUpdate(ChannelBase):
    name: str | None = Field(max_length=100)
    type: ChannelType | None = Field(max_length=100)


# Properties to return to client
class Channel(ChannelBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    server_id: uuid.UUID = Field(foreign_key="server.id", nullable=False)
    server: Server = Relationship(back_populates="channels")
    messages: list["Message"] = Relationship(back_populates="channel", cascade_delete=True)


# Shared properties
class MessageBase(SQLModel):
    content: str = Field(max_length=1000, nullable=False)


# Properties to receive via API on creation
class MessageCreate(MessageBase):
    pass


# Properties to receive via API on update
class MessageUpdate(MessageBase):
    content: str | None = Field(max_length=1000)


# Properties to return to client
class Message(MessageBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    author_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    channel_id: uuid.UUID = Field(foreign_key="channel.id", nullable=False, ondelete="CASCADE")
    channel: Channel = Relationship(back_populates="messages")


# Jwt token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Jwt token data
class TokenData(SQLModel):
    sub: str | None = None