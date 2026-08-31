from app.schemas.models.enums.role import Role
from app.schemas.models.user import User


class Admin(User):
    __role : Role = Role.ADMIN