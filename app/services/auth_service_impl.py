from app.services.auth_services import AuthServices

from app.schemas.requests.register_user_request import RegisterUserRequest
from app.schemas.requests.login_user_request import LoginUserRequest

from app.schemas.responses.register_user_response import RegisterUserResponse
# from app.schemas.responses.login_user_response import LoginUserResponse
# from app.schemas.responses.logout_user_response import LogoutUserResponse

from app.schemas.models.user import User
from app.repositories.user_repository import UserRepository


class AuthServiceImpl(AuthServices):

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(
            self,
            register_user_request: RegisterUserRequest
    ) -> RegisterUserResponse:


        existing_user = self.user_repository.find_by_email(
            register_user_request.email
        )

        if existing_user:
            raise ValueError("User already exists")


        user = User(
            first_name=register_user_request.first_name,
            last_name=register_user_request.last_name,
            email=register_user_request.email,
            phone=register_user_request.phone,
            username=register_user_request.username,
            password=register_user_request.password
        )


        saved_user = self.user_repository.save(user)


        return RegisterUserResponse(
            id=saved_user.id,
            first_name=saved_user.first_name,
            last_name=saved_user.last_name,
            email=saved_user.email,
            phone=saved_user.phone,
            username=saved_user.username
        )

    # def login_user(
    #         self,
    #         login_user_request: LoginUserRequest
    # ) -> LoginUserResponse:
    #
    #
    #     user = self.user_repository.find_by_username(
    #         login_user_request.username
    #     )
    #
    #     if user is None:
    #         raise ValueError("Invalid username or password")
    #
    #
    #     if user.password != login_user_request.password:
    #         raise ValueError("Invalid username or password")
    #
    #     return LoginUserResponse(
    #         id=user.id,
    #         username=user.username,
    #         message="Login successful"
    #     )
    #
    # def logout_user(self) -> LogoutUserResponse:
    #
    #     return LogoutUserResponse(
    #         message="Logout successful"
    #     )