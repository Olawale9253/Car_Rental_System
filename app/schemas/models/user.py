import uuid
from abc import ABC
from uuid import UUID

from sqlmodel import SQLModel ,Field

from app.schemas.models.enums.role import Role

class User(ABC,SQLModel,table=True):
    id: UUID = Field(default_factory=uuid.uuid4,primary_key=True)
    full_name : str
    username : str = Field(unique=True)
    email : str = Field(unique=True)
    password : str
    role : Role
    is_logged_in: bool = False
