import datetime
import uuid
from enum import StrEnum

from pydantic import BaseModel, EmailStr


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
    user_agent: str  # TODO правильно доставать юзер агент
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
    session_id: str


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
    session_id: str


class HistorySchema(BaseModel):
    id: uuid.UUID
    auth_date: datetime.datetime
    user_agent: str


class UserHistoryResponseSchema(BaseModel):
    user_id: uuid.UUID
    user_history: list[HistorySchema]
