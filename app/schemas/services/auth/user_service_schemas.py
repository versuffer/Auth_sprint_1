import uuid

from pydantic import BaseModel

from app.schemas.api.v1.auth_schemas import RegisterResponseSchema
from app.schemas.api.v1.roles_schemas import RolesSchema


class UserCreatedSchema(RegisterResponseSchema):
    pass


class UserDBSchema(BaseModel):
    login: str
    hashed_password: str
    roles: RolesSchema
    id: uuid.UUID
    is_superuser: bool
