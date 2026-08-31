import uuid

from app.schemas.models.enums.role import Role

from sqlmodel import SQLModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from decimal import Decimal

class Rental(SQLModel,table=True):
    id : UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    car_id : UUID = Field(foreign_key='car.id')
    customer_name : str
    customer_phone_number : str
    customer_address : str
    customer_email : str
    sold_by_id: UUID = Field(foreign_key='user.id',index=True)
    sold_by_name : str
    user_role : Role
    price : Decimal
    rental_datetime : datetime = Field(default_factory=datetime.now)
    expected_return_date : Optional[datetime] = None
    actual_return_date: Optional[datetime] = None
    is_active: bool = Field(default=True)