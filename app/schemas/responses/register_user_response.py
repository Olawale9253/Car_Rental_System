from typing import Optional

from pydantic import BaseModel

from app.schemas.models.enums.role import Role

class RegisterUserResponse(BaseModel):
    user_id : Optional[int] = None
    username : str = None
    email : str = None
    role : Role = None
    message : Optional[str] = None
