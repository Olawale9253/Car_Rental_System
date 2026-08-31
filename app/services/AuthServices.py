from abc import ABC, abstractmethod

from app.schemas.models import RegisterUserRequest, RegisterUserResponse, LoginUserRequest, LoginUserResponse


class AuthServices(ABC):
    @abstractmethod
    def register_user(self, register_user_request: RegisterUserRequest) -> RegisterUserResponse:
        pass

    @abstractmethod
    def login_user(self,login_user_request: LoginUserRequest ) -> LoginUserResponse:
        pass

    @abstractmethod
    def logout_user(self):
        pass