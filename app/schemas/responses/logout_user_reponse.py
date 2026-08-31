from pydantic import BaseModel

class LoginUserResponse(BaseModel):
    message : str = None
