from typing import Optional

from pydantic import BaseModel

class UpdateUserRequest(BaseModel):
    username : Optional[str] = None
    email : Optional[str] = None
    full_name : Optional[str] = None
    password : Optional[str] = None
