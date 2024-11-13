import uuid
from enum import Enum
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship

# Shared properties
class UserBase(SQLModel, table=True):
    username: str
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_super_admin: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=255)


# Properties to receive via API on update
class UserUpdate(UserBase):
    username: str | None
    email: EmailStr | None = Field(default="none", max_length=255)
    password: str | None = Field(min_length=8, max_length=255)


# Properties to return to client
class User(UserBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    owned_servers: list["Server"] = Relationship(back_populates="owner")
    servers: list["Server"] = Relationship(back_populates="members")


# Shared properties
class ServerBase(SQLModel, table=True):
    name: str | None = Field(max_length=100)


# Properties to receive via API on creation
class ServerCreate(ServerBase):
    pass


# Properties to receive via API on update
class ServerUpdate(ServerBase):
    name: str | None = Field(max_length=100)


# Properties to return to client
class Server(ServerBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    owner: User = Relationship(back_populates="owned_servers")
    admins: list["User"] | None = Relationship(back_populates="servers")
    members: list["User"] = Relationship(back_populates="servers")
    channels: list["Channel"] = Relationship(back_populates="server")


# Define the accepted channel types
class ChannelType(str, Enum):
    TEXT = "text"
    VOICE = "voice"


# Shared properties
class ChannelBase(SQLModel, table=True):
    name: str = Field(max_length=100, required=True)
    type: ChannelType = Field(max_length=100, required=True)


# Properties to receive via API on creation
class ChannelCreate(ChannelBase):
    pass


# Properties to receive via API on update
class ChannelUpdate(ChannelBase):
    name: str | None = Field(max_length=100)
    type: ChannelType | None = Field(max_length=100)


# Properties to return to client
class Channel(ChannelBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    server_id: uuid.UUID = Field(foreign_key="server.id", nullable=False)
    server: Server = Relationship(back_populates="channels")
    messages: list["Message"] = Relationship(back_populates="channel")


# Shared properties
class MessageBase(SQLModel, table=True):
    content: str = Field(max_length=1000, required=True)


# Properties to receive via API on creation
class MessageCreate(MessageBase):
    pass


# Properties to receive via API on update
class MessageUpdate(MessageBase):
    content: str | None = Field(max_length=1000, required=True)


# Properties to return to client
class Message(MessageBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    author_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)