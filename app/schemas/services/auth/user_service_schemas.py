import uuid

from pydantic import BaseModel, Field, ConfigDict

from app.schemas.api.v1.auth_schemas import RegisterResponseSchema
from app.schemas.api.v1.roles_schemas import RolesSchema, RoleSchema


class UserCreatedSchema(RegisterResponseSchema):
    pass


class UserDBSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: str
    hashed_password: str
    roles: list[RoleSchema] = []
    id: uuid.UUID
    is_superuser: bool
