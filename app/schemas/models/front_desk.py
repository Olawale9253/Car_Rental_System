from app.schemas.models.enums.role import Role
from app.schemas.models.user import User


class FrontDesk(User):
    __role : Role = Role.FRONT_DESK