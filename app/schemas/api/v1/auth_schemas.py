import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class UserCredentialsSchema(BaseModel):
    login: str
    password: str


class UserNewSchema(BaseModel):

    username: str
    email: str
    hashed_password: str


class UserLoginCredentialsSchema(UserCredentialsSchema):
    user_agent: str  # TODO правильно доставать юзер агент


class UserRefreshCredentialsSchema(BaseModel):
    refresh_token: str
    user_agent: str


class UserTokensCredentialsSchema(BaseModel):
    login: str
    roles: list[str]


class UserTokensSchema(BaseModel):
    refresh_token: str
    access_token: str


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
