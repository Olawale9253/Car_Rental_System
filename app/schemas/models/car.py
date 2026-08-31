import uuid
from uuid import UUID

from sqlmodel import SQLModel, Field
from app.schemas.models.enums.car_brand import CarBrand
from app.schemas.models.enums.car_model import CarModel
from app.schemas.models.enums.car_state import CarState
from app.schemas.models.enums.release_year import ReleaseYear

class Car(SQLModel, table=True):
    id : UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    brand: CarBrand
    model : CarModel
    release_year: ReleaseYear
    plate_number: str = Field(unique=True)
    car_state : CarState = Field(default=CarState.AVAILABLE)