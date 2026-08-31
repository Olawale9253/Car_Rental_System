import uuid

import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import  Session

from app.schemas.models.enums.role import Role
from app.schemas.models.user import User
from app.repositories.user_repository import UserRepository

class TestUserRepository:

    @pytest.fixture
    def repository(self,session:Session) -> UserRepository:
        return UserRepository(session=session)

    def test_empty_repository(self,repository : UserRepository) -> None:

        assert repository is not None

    def test_save_user_count_is_one(self,repository: UserRepository) -> None:

        user = User()

        user.full_name = 'onwere grace'
        user.email = 'lifeisTuff@gmail.com'
        user.password = '453244566'
        user.username = 'gracey'
        user.role = Role.FRONT_DESK

        repository.save(user)

        assert repository.count() == 1
        assert user.id is not None

    def test_save_user_with_duplicate_email_raises_integrity_error(self, repository :UserRepository) -> None:


        user = User()
        user.full_name = 'onwere grace'
        user.email = 'lifeisTuff@gmail.com'
        user.password = '453244566'
        user.username = 'gracey'
        user.role = Role.FRONT_DESK
        repository.save(user)

        user_two = User()

        user_two.full_name = 'onwere grace'
        user_two.email = 'lifeisTuff@gmail.com'
        user_two.password = '453244566'
        user_two.username = 'fakegrace'
        user_two.role = Role.FRONT_DESK

        with pytest.raises(IntegrityError):
            repository.save(user_two)

    def test_save_two_users_count_is_two(self,repository : UserRepository)->None:

        user = User()
        user.full_name = 'onwere grace'
        user.email = 'lifeisTuff@gmail.com'
        user.password = '453244566'
        user.username = 'gracey'
        user.role = Role.FRONT_DESK
        repository.save(user)

        user_two = User()

        user_two.full_name = 'Nwababy'
        user_two.email = 'lifeisSoft@gmail.com'
        user_two.password = '453244566'
        user_two.username = 'fakegrace'
        user_two.role = Role.ADMIN
        repository.save(user_two)

        assert repository.count() == 2

    def test_save_user_with_duplicate_username_raises_integrity_error(self, repository : UserRepository) -> None:

        user = User()
        user.full_name = 'onwere grace'
        user.email = 'lifeisTuff@gmail.com'
        user.password = '453244566'
        user.username = 'gracey'
        user.role = Role.FRONT_DESK
        repository.save(user)

        user_two = User()

        user_two.full_name = 'onwere grace'
        user_two.email = 'lifeisTuff@gmail.com'
        user_two.password = '453244566'
        user_two.username = 'gracey'
        user_two.role = Role.FRONT_DESK

        with pytest.raises(IntegrityError):
            repository.save(user_two)

    def test_save_user_with_missing_required_fields_raises_integrity_error(self, repository : UserRepository) -> None:

        user = User()
        user.email = 'lifeisTuff@gmail.com'
        user.password = '453244566'
        user.username = 'gracey'
        user.role = Role.FRONT_DESK

        with pytest.raises(IntegrityError):
            repository.save(user)

    def test_find_by_id_returns_valid_user(self,repository : UserRepository) -> None:

        user = User()
        user.full_name = 'onwere grace'
        user.email = 'lifeisTuff@gmail.com'
        user.password = '453244566'
        user.username = 'gracey'
        user.role = Role.FRONT_DESK
        repository.save(user)

        assert repository .find_by_id(user.id) == user

    def test_find_by_id_returns_none(self,repository : UserRepository) -> None:

        fake_id = (uuid.uuid4())

        assert repository.find_by_id(fake_id) is None

    def test_find_by_id_returns_correct_data_types(self,repository : UserRepository) -> None:

        user = User()
        user.full_name = 'onwere grace'
        user.email = 'lifeisTuff@gmail.com'
        user.password = '453244566'
        user.username = 'gracey'
        user.role = Role.FRONT_DESK
        repository.save(user)

        retrieved_user = repository.find_by_id(user.id)

        assert retrieved_user.role == Role.FRONT_DESK

    # def test_update_user_fullname_changed(self,session: Session) -> None:
    #     repository = UserRepository(session=session)
    #
    #     user = User()
    #     user.full_name = 'onwere grace'
    #     user.email = 'lifeisTuff@gmail.com'
    #     user.password = '453244566'
    #     user.username = 'gracey'
    #     user.role = Role.FRONT_DESK
    #     repository.save(user)
    #
    #     saved_user_id = user.id
    #
    #     update_data = {'full_name': 'Nwababy'}
    #
    #     repository.update_by_id(saved_user_id, update_data)
    #
    #     assert user.full_name == 'Nwababy'

    # def test_update_non_existing_user_returns_none(self,session: Session) -> None:
    #     repository = UserRepository(session=session)
    #
    #     fake_id = (uuid.uuid4())
    #
    #     update_data = {'full_name': 'Nwababy'}
    #
    #     saved_user = repository.update_by_id(fake_id, update_data)
    #
    #     assert saved_user is None

    def test_delete_by_id_returns_true(self,repository : UserRepository) -> None:

        user = User()
        user.full_name = 'onwere grace'
        user.email = 'lifeisTuff@gmail.com'
        user.password = '453244566'
        user.username = 'gracey'
        user.role = Role.FRONT_DESK
        repository.save(user)

        assert repository.delete_by_id(user.id) is True
        assert repository.find_by_id(user.id) is None

    def test_delete_non_existent_id_returns_false(self,repository :UserRepository) -> None:

        fake_id = (uuid.uuid4())

        assert repository.delete_by_id(fake_id) is False

    def test_save_two_users_delete_one_user_count_is_one(self,repository :UserRepository) -> None:

        user = User()
        user.full_name = 'onwere grace'
        user.email = 'lifeisTuff@gmail.com'
        user.password = '453244566'
        user.username = 'gracey'
        user.role = Role.FRONT_DESK
        repository.save(user)

        user_two = User()

        user_two.full_name = 'Nwababy'
        user_two.email = 'lifeisSoft@gmail.com'
        user_two.password = '453244566'
        user_two.username = 'fakegrace'
        user_two.role = Role.ADMIN
        repository.save(user_two)

        assert repository.count() == 2

        repository.delete_by_id(user.id)

        assert repository.count() == 1