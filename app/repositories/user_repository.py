from uuid import UUID

from sqlmodel import Session, select

from app.schemas.models.user import User


class UserRepository:
    def __init__(self,session: Session):
        self._session = session

    def save(self,user: User) -> User:
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def find_by_id(self,user_id: UUID):
        return self._session.get(User,user_id)

    def find_all(self):
        statement = select(User)
        return self._session.exec(statement).all()

    def delete_by_id(self,user_id: UUID) -> bool:
        user = self.find_by_id(user_id)

        if user is not None:
            self._session.delete(user)
            self._session.commit()
            return True
        return False

    # def update_by_id(self,user_id: UUID,request_dto: UpdateUserRequest):
    #     user = self.find_by_id(user_id)
    #     if user is None:
    #         return None

        update_data = request_dto.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(user, key, value)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)

        return user

    def count (self) -> int:
        users = self.find_all()
        return len(users)

