from app.schemas.models.enums.role import Role
from app.schemas.models.user import User

class FleetManager(User):
    __role : Role = Role.FLEET_MANAGER

