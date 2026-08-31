from pydantic import BaseModel, Field

class LoginUserRequest(BaseModel):
    username : str = Field(...,min_length=1,max_length=20)
    password : str = Field(...,min_length=8,max_length=20)
