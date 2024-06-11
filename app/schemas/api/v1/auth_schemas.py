import uuid

from pydantic import BaseModel


class UserCredentialsSchema(BaseModel):
    login: str
    password: str


class RegisterResponseSchema(BaseModel):
    id: uuid.UUID
    login: str
    is_super_user: bool
