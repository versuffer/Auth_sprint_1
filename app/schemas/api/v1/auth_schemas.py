import datetime
import uuid

from pydantic import BaseModel


class UserCredentialsSchema(BaseModel):
    login: str
    password: str


class UserNewSchema(BaseModel):

    username: str
    email: str
    hashed_password: str


class BaseLoginDataSchema(BaseModel):
    user_agent: str  # TODO правильно доставать юзер агент


class CredentialsLoginDataSchema(BaseLoginDataSchema, UserCredentialsSchema):
    pass


class RefreshLoginDataSchema(BaseLoginDataSchema):
    refresh_token: str


class UserTokenDataSchema(BaseModel):
    login: str
    roles: list[str]


class UserTokensSchema(BaseModel):
    access_token: str
    refresh_token: str


class ResetUsernameSchema(BaseModel):
    login: str
    new_username: str


class ResetPasswordSchema(BaseModel):
    login: str
    current_password: str
    new_password: str


class RegisterResponseSchema(BaseModel):
    id: uuid.UUID
    login: str
    is_superuser: bool


class HistorySchema(BaseModel):
    id: uuid.UUID
    auth_date: datetime.datetime
    user_agent: str


class UserHistoryResponseSchema(BaseModel):
    user_id: uuid.UUID
    user_history: list[HistorySchema]
