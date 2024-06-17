import uuid

from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.services.auth.role_service_schemas import RoleSchema


class UserDBSchema(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    roles: list[RoleSchema] = []
    id: uuid.UUID
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)
