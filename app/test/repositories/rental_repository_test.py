import uuid
from datetime import datetime
from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import text
from sqlmodel import Session

from app.schemas.models.car import Car
from app.schemas.models.enums.car_brand import CarBrand
from app.schemas.models.enums.car_model import CarModel
from app.schemas.models.enums.car_state import CarState
from app.schemas.models.enums.release_year import ReleaseYear
from app.schemas.models.rental import Rental
from app.schemas.models.enums.role import Role
from app.schemas.models.user import User
from app.repositories.car_repository import CarRepository
from app.repositories.rental_repository import RentalRepository
from app.repositories.user_repository import UserRepository


class TestRentalRepository:

    @pytest.fixture
    def setup_dependencies(self,session: Session):
        car_repository = CarRepository(session=session)
        user_repository = UserRepository(session=session)

        car = Car()
        car.brand = CarBrand.TOYOTA
        car.model = CarModel.CAMRY
        car.release_year = ReleaseYear.YEAR_2015
        car.plate_number = "0101"
        car.car_state = CarState.AVAILABLE

        car_repository.save(car)

        user = User()
        user.full_name = 'onwere grace'
        user.email = 'lifeisTuff@gmail.com'
        user.password = '453244566'
        user.username = 'gracey'
        user.role = Role.FRONT_DESK

        user_repository.save(user)

        return car,user

    def test_empty_repository(self,session: Session):
        rental_repository = RentalRepository(session=session)

        assert rental_repository is not None

    def test_save_rental_count_is_one(self,session: Session,setup_dependencies : tuple):

        car,user = setup_dependencies
        rental_repository = RentalRepository(session=session)

        rental = Rental()
        rental.car_id = car.id
        rental.customer_name = 'Okoro'
        rental.customer_phone_number = '08166345689'
        rental.customer_address = 'Mushin'
        rental.customer_email = 'okorobobo@yahoo.com'
        rental.sold_by_id = user.id
        rental.sold_by_name = user.username
        rental.user_role = user.role
        rental.price = Decimal(10000)
        rental.rental_datetime = datetime.now()

        rental_repository.save(rental)

        assert rental_repository.count() == 1

    def test_save_rental_missing_car_foreign_key_raises_error(self,session: Session,setup_dependencies : tuple):
        session.exec(text("PRAGMA foreign_keys=ON"))
        _,user = setup_dependencies
        rental_repository = RentalRepository(session=session)

        rental = Rental()
        rental.car_id = uuid.uuid4()
        rental.customer_name = 'Ghost'
        rental.customer_phone_number = '08166345689'
        rental.customer_address = 'Ajah'
        rental.customer_email = 'catchmeifyoucan@gmail.com'
        rental.sold_by_id = user.id
        rental.sold_by_name = user.username
        rental.user_role = user.role
        rental.price = Decimal(10000)

        with pytest.raises(IntegrityError):
            rental_repository.save(rental)

    def test_find_all_active_rentals(self,session: Session,setup_dependencies : tuple):
            car, user = setup_dependencies
            rental_repository = RentalRepository(session=session)

            rental = Rental()
            rental.car_id = car.id
            rental.customer_name = 'Okoro'
            rental.customer_phone_number = '08166345689'
            rental.customer_address = 'Mushin'
            rental.customer_email = 'okorobobo@yahoo.com'
            rental.sold_by_id = user.id
            rental.sold_by_name = user.username
            rental.user_role = user.role
            rental.price = Decimal(10000)
            rental.rental_datetime = datetime.now()

            rental_repository.save(rental)

            rental_two = Rental()
            rental_two.car_id = car.id
            rental_two.customer_name = 'Okoro'
            rental_two.customer_phone_number = '08166345689'
            rental_two.customer_address = 'Mushin'
            rental_two.customer_email = 'okorobobo@yahoo.com'
            rental_two.sold_by_id = user.id
            rental_two.sold_by_name = user.username
            rental_two.user_role = user.role
            rental_two.price = Decimal(10000)
            rental_two.rental_datetime = datetime.now()

            rental_repository.save(rental_two)

            assert rental_repository.count() == 2
            assert len(rental_repository.find_active()) == 2