from uuid import UUID

from sqlmodel import Session, select

from app.schemas.models.rental import Rental

class RentalRepository:
    def __init__(self, session: Session):
        self._session = session

    def save(self,rental: Rental):
        self._session.add(rental)
        self._session.commit()
        self._session.refresh(rental)
        return rental

    def find_by_id(self,rental_id: UUID):
       return self._session.get(Rental,rental_id)

    def find_all(self):
        rentals = select(Rental)
        return self._session.exec(rentals).all()

    def delete_by_id(self,rental_id: UUID) -> bool:
        rental = self.find_by_id(rental_id)

        if rental is not None:
            self._session.delete(rental)
            self._session.commit()
            return True
        return False

    def count(self):
        rentals = self.find_all()
        return len(rentals)

    def find_active(self):
        statement = select(Rental).where(Rental.is_active==True)
        return self._session.exec(statement).all()