from fastapi import APIRouter, Depends, HTTPException, status

from app.api.docs.tags import ApiTags
from app.exceptions import UserAlreadyExistError, UserNotFoundError, WrongPasswordError
from app.schemas.api.v1.auth_schemas import (
    CredentialsLoginDataSchema,
    RefreshLoginDataSchema,
    RegisterResponseSchema,
    UserCredentialsSchema,
    UserTokensSchema,
)
from app.services.auth.auth_service import AuthenticationService
from app.services.auth.registration_service import RegistrationService

auth_router = APIRouter(prefix='/auth')


@auth_router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    summary='Зарегистрировать пользователя',
    response_model=RegisterResponseSchema,
    tags=[ApiTags.V1_AUTH],
)
async def register(
    user_credentials: UserCredentialsSchema,
    service: RegistrationService = Depends(),
):
    try:
        if user := await service.create_user(user_credentials):
            return user
    except UserAlreadyExistError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@auth_router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    summary='Аутентифицировать пользователя по логину и паролю',
    response_model=UserTokensSchema,
    tags=[ApiTags.V1_AUTH],
)
async def login(
    user_credentials: CredentialsLoginDataSchema,
    service: AuthenticationService = Depends(),
):
    try:
        return await service.authenticate_by_credentials(user_credentials)
    except WrongPasswordError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Неверный пароль')
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Пользователя с таким логином не существует.'
        )


@auth_router.post(
    '/refresh',
    status_code=status.HTTP_200_OK,
    summary='Аутентифицировать пользователя по refresh-токену',
    response_model=UserTokensSchema,
    tags=[ApiTags.V1_AUTH],
)
async def refresh(
    user_credentials: RefreshLoginDataSchema,
    service: AuthenticationService = Depends(),
):
    try:
        return await service.authenticate_by_refresh_token(user_credentials)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Пользователя с таким логином не существует.'
        )


@auth_router.post(
    '/logout',
    status_code=status.HTTP_200_OK,
    summary='Инвалидировать сессию пользователя по access-токену',
    tags=[ApiTags.V1_AUTH],
)
async def logout(
    access_token: str,  # TODO
    service: AuthenticationService = Depends(),
):
    return {'session_id': await service.logout(access_token)}


@auth_router.post(
    '/verify_access_token',
    status_code=status.HTTP_200_OK,
    summary='Проверить пользователя по access-токену',
    tags=[ApiTags.V1_AUTH],
)
async def verify_access_token(
    access_token: str,  # TODO
    service: AuthenticationService = Depends(),
):
    if not service.verify_access_token(access_token):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@auth_router.post(
    '/reset/username',
    status_code=status.HTTP_200_OK,
    summary='Поменять имя пользователя',
    # response_model=ResetUsernameResponseSchema,
    tags=[ApiTags.V1_AUTH],
)
async def reset_username(
    # reset_schema: ResetUsernameSchema,
    # access_token: AuthorizationHeader,
):
    pass


@auth_router.post(
    '/reset/password',
    status_code=status.HTTP_200_OK,
    summary='Поменять пароль пользователя',
    # response_model=ResetPasswordResponseSchema,
    tags=[ApiTags.V1_AUTH],
)
async def reset_password(
    # reset_schema: ResetPasswordSchema,
    # access_token: AuthorizationHeader,
):
    pass


@auth_router.get(
    '/history',
    status_code=status.HTTP_200_OK,
    summary='Получить историю входов пользователя',
    # response_model=ResetPasswordResponseSchema,
    tags=[ApiTags.V1_AUTH],
)
async def get_history(
    # access_token: AuthorizationHeader,
):
    pass
