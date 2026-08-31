import pytest
from app.schemas.requests.register_user_request import RegisterUserRequest
from app.schemas.requests.login_user_request import LoginUserRequest


from app.services.auth_service_impl import AuthServiceImpl


class TestAuthService:

    def setup_method(self):

        self.auth_service = AuthServiceImpl()

    def test_register_user(self):

        request = RegisterUserRequest(
            first_name="Taofeek",
            last_name="Olawale",
            email="taofeek@gmail.com",
            phone="08012345678",
            username="taofeek",
            password="password123"
        )


        response = self.auth_service.register_user(request)


        assert response is not None
        assert response.email == "taofeek@gmail.com"

    def test_login_user(self):

        register_request = RegisterUserRequest(
            first_name="Taofeek",
            last_name="Olawale",
            email="taofeek@gmail.com",
            phone="08012345678",
            username="taofeek",
            password="password123"
        )

        self.auth_service.register_user(register_request)

        login_request = LoginUserRequest(
            username="taofeek",
            password="password123"
        )


        response = self.auth_service.login_user(login_request)

        assert response is not None

    def test_logout_user(self):

        result = self.auth_service.logout_user()

        assert result is None