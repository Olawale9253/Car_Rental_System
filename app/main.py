from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from app.core.database import create_db_and_tables, get_session
from app.repositories.user_repository import UserRepository
from app.schemas.models.car import Car
from app.schemas.models.rental import Rental
from app.schemas.models.user import User
from app.schemas.models.enums.car_brand import CarBrand
from app.schemas.models.enums.car_model import CarModel
from app.schemas.models.enums.car_state import CarState
from app.schemas.models.enums.release_year import ReleaseYear
from app.schemas.models.enums.role import Role


class RegisterRequest(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    email: str
    password: str = Field(min_length=8)
    phone: str = ""
    username: Optional[str] = None
    role: str = "FRONT_DESK"


class LoginRequest(BaseModel):
    email: str
    password: str


class CarRequest(BaseModel):
    brand: str
    model: str
    release_year: int
    plate_number: str
    daily_price: float = Field(default=0, ge=0)
    car_state: str = "AVAILABLE"


class RentalRequest(BaseModel):
    car_id: str
    customer_name: str
    customer_phone_number: str
    customer_address: str = ""
    customer_email: str
    price: float = Field(ge=0)
    expected_return_date: Optional[datetime] = None


app = FastAPI(title="Car Rental Service API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
create_db_and_tables()


@app.on_event("startup")
def startup() -> None:
    create_db_and_tables()


def user_payload(user: User) -> dict:
    return {
        "id": str(user.id),
        "email": user.email,
        "name": user.full_name,
        "username": user.username,
        "role": user.role.name,
    }


def car_payload(car: Car) -> dict:
    return {
        "id": str(car.id),
        "brand": car.brand.name,
        "model": car.model.name,
        "release_year": car.release_year.value,
        "plate_number": car.plate_number,
        "daily_price": float(car.daily_price),
        "car_state": car.car_state.name,
    }


def rental_payload(rental: Rental) -> dict:
    return {
        "id": str(rental.id),
        "car_id": str(rental.car_id),
        "customer_name": rental.customer_name,
        "customer_phone_number": rental.customer_phone_number,
        "customer_address": rental.customer_address,
        "customer_email": rental.customer_email,
        "price": float(rental.price),
        "rental_datetime": rental.rental_datetime.isoformat(),
        "expected_return_date": rental.expected_return_date.isoformat() if rental.expected_return_date else None,
        "actual_return_date": rental.actual_return_date.isoformat() if rental.actual_return_date else None,
        "is_active": rental.is_active,
    }


def enum_value(enum_type, value):
    try:
        return enum_type[value.upper()]
    except KeyError as error:
        raise HTTPException(status_code=422, detail=f"Invalid {enum_type.__name__}: {value}") from error


def car_values(request: CarRequest) -> dict:
    try:
        release_year = ReleaseYear(request.release_year)
    except ValueError as error:
        raise HTTPException(status_code=422, detail="Invalid release year") from error
    return {
        "brand": enum_value(CarBrand, request.brand),
        "model": enum_value(CarModel, request.model),
        "release_year": release_year,
        "plate_number": request.plate_number,
        "daily_price": request.daily_price,
        "car_state": enum_value(CarState, request.car_state),
    }


@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, session: Session = Depends(get_session)):
    repository = UserRepository(session)
    username = request.username or request.email.split("@")[0]
    if repository.find_by_email(request.email) or repository.find_by_username(username):
        raise HTTPException(status_code=409, detail="An account with that email or username already exists")

    user = User(
        full_name=f"{request.first_name} {request.last_name}".strip(),
        username=username,
        email=request.email,
        password=request.password,
        role=enum_value(Role, request.role),
    )
    saved_user = repository.save(user)
    return {"user": user_payload(saved_user), "message": "Account created successfully"}


@app.post("/api/auth/login")
def login(request: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == request.email)).first()
    if user is None or user.password != request.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    user.is_logged_in = True
    session.add(user)
    session.commit()
    return {"user": user_payload(user), "message": "Login successful"}


@app.post("/api/auth/logout")
def logout(email: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == email)).first()
    if user:
        user.is_logged_in = False
        session.add(user)
        session.commit()
    return {"message": "Logout successful"}


@app.get("/api/cars")
def list_cars(session: Session = Depends(get_session)):
    return [car_payload(car) for car in session.exec(select(Car)).all()]


@app.post("/api/cars", status_code=status.HTTP_201_CREATED)
def create_car(request: CarRequest, session: Session = Depends(get_session)):
    values = car_values(request)
    if session.exec(select(Car).where(Car.plate_number == request.plate_number)).first():
        raise HTTPException(status_code=409, detail="A car with that plate number already exists")
    car = Car(**values)
    session.add(car)
    session.commit()
    session.refresh(car)
    return car_payload(car)


@app.put("/api/cars/{car_id}")
def update_car(car_id: str, request: CarRequest, session: Session = Depends(get_session)):
    car = session.get(Car, UUID(car_id))
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    values = car_values(request)
    duplicate = session.exec(
        select(Car).where(Car.plate_number == request.plate_number, Car.id != car.id)
    ).first()
    if duplicate:
        raise HTTPException(status_code=409, detail="A car with that plate number already exists")
    for key, value in values.items():
        setattr(car, key, value)
    session.add(car)
    session.commit()
    session.refresh(car)
    return car_payload(car)


@app.delete("/api/cars/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(car_id: str, session: Session = Depends(get_session)):
    car = session.get(Car, UUID(car_id))
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    active_rental = session.exec(select(Rental).where(Rental.car_id == car.id, Rental.is_active == True)).first()
    if active_rental:
        raise HTTPException(status_code=409, detail="Active rentals must be completed before deleting this car")
    session.delete(car)
    session.commit()


@app.post("/api/rentals", status_code=status.HTTP_201_CREATED)
def create_rental(request: RentalRequest, session: Session = Depends(get_session)):
    car = session.get(Car, UUID(request.car_id))
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    if car.car_state != CarState.AVAILABLE:
        raise HTTPException(status_code=409, detail="Car is not available")
    admin = session.exec(select(User).where(User.is_logged_in == True)).first()
    if admin is None:
        raise HTTPException(status_code=401, detail="An authenticated admin is required")
    rental = Rental(
        car_id=car.id,
        customer_name=request.customer_name,
        customer_phone_number=request.customer_phone_number,
        customer_address=request.customer_address,
        customer_email=request.customer_email,
        sold_by_id=admin.id,
        sold_by_name=admin.full_name,
        user_role=admin.role,
        price=request.price,
        expected_return_date=request.expected_return_date,
    )
    car.car_state = CarState.RENTED
    session.add(rental)
    session.add(car)
    session.commit()
    session.refresh(rental)
    return rental_payload(rental)


@app.get("/api/rentals")
def list_rentals(session: Session = Depends(get_session)):
    return [rental_payload(rental) for rental in session.exec(select(Rental)).all()]


@app.put("/api/rentals/{rental_id}/complete")
def complete_rental(rental_id: str, session: Session = Depends(get_session)):
    rental = session.get(Rental, UUID(rental_id))
    if rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    rental.is_active = False
    rental.actual_return_date = datetime.now()
    car = session.get(Car, rental.car_id)
    if car:
        car.car_state = CarState.AVAILABLE
        session.add(car)
    session.add(rental)
    session.commit()
    session.refresh(rental)
    return rental_payload(rental)


@app.delete("/api/rentals/{rental_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rental(rental_id: str, session: Session = Depends(get_session)):
    rental = session.get(Rental, UUID(rental_id))
    if rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    if rental.is_active:
        car = session.get(Car, rental.car_id)
        if car:
            car.car_state = CarState.AVAILABLE
            session.add(car)
    session.delete(rental)
    session.commit()


@app.get("/api/dashboard")
def dashboard(session: Session = Depends(get_session)):
    cars = session.exec(select(Car)).all()
    rentals = session.exec(select(Rental)).all()
    return {
        "available_cars": sum(car.car_state == CarState.AVAILABLE for car in cars),
        "active_rentals": sum(rental.is_active for rental in rentals),
        "total_fleet": len(cars),
        "revenue": sum(float(rental.price) for rental in rentals),
    }


def main():
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()
