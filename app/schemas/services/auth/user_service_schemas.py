import uuid

from pydantic import BaseModel

from app.schemas.api.v1.auth_schemas import RegisterResponseSchema


class UserCreatedSchema(RegisterResponseSchema):
    pass


class UserDBSchema(BaseModel):
    login: str
    hashed_password: str
    dynamic_salt: str
    roles: list[str]
    id: uuid.UUID
    is_superuser: bool
