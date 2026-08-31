import pytest
from sqlalchemy import create_engine, delete
from sqlmodel import SQLModel, Session

from app.schemas.models.car import Car
from app.schemas.models.rental import Rental
from app.schemas.models.user import User

TEST_DATABASE_URL : str = 'sqlite:///./test.db'

test_engine = create_engine(TEST_DATABASE_URL, echo=True)

@pytest.fixture
def session():
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        session.exec(delete(User))
        session.exec(delete(Car))
        session.exec(delete(Rental))
        yield session