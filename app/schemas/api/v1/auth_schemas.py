import datetime
import uuid
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginType(StrEnum):
    CREDENTIALS = 'credentials'
    REFRESH = 'refresh'


class UserCredentialsSchema(BaseModel):
    login: str
    password: str


class RegisterUserCredentialsSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserNewSchema(BaseModel):
    username: str
    email: str
    hashed_password: str


class BaseLoginDataSchema(BaseModel):
    user_agent: str
    login_type: LoginType


class CredentialsLoginDataSchema(BaseLoginDataSchema, UserCredentialsSchema):
    pass


class RefreshLoginDataSchema(BaseLoginDataSchema):
    refresh_token: str


class UserTokenDataSchema(BaseModel):
    login: str
    roles: list[str]


class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str


class SessionDataSchema(TokenPairSchema):
    session_id: uuid.UUID


class ResetUsernameSchema(BaseModel):
    login: str
    new_username: str


class ResetPasswordSchema(BaseModel):
    login: str
    current_password: str
    new_password: str


class RegisterResponseSchema(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    is_superuser: bool


class HistorySchemaCreate(BaseModel):
    user_id: uuid.UUID
    auth_date: datetime.datetime
    user_agent: str
    login_type: LoginType
    session_id: uuid.UUID


class HistorySchema(BaseModel):
    id: uuid.UUID
    auth_at: datetime.datetime = Field(serialization_alias='auth_date')  # TODO поменять в миграции на auth_date
    user_agent: str

    model_config = ConfigDict(from_attributes=True)


class HistoryResponseSchema(HistorySchema):
    pass
