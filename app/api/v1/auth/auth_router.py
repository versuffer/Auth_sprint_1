from fastapi import APIRouter, status

from app.api.docs.tags import ApiTags

auth_router = APIRouter(prefix='/auth')


@auth_router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    summary='Зарегистрировать пользователя',
    # response_model=RegisterResponseSchema,
    tags=[ApiTags.V1_AUTH],
)
async def register(
    # user_credentials: UserCredentialsSchema,
):
    pass


@auth_router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    summary='Аутентифицировать пользователя по логину и паролю',
    # response_model=LoginResponseSchema,
    tags=[ApiTags.V1_AUTH],
)
async def login(
    # user_credentials: UserCredentialsSchema,
):
    pass


@auth_router.post(
    '/refresh',
    status_code=status.HTTP_200_OK,
    summary='Аутентифицировать пользователя по refresh-токену',
    # response_model=RefreshResponseSchema,
    tags=[ApiTags.V1_AUTH],
)
async def refresh(
    # refresh_token: AuthorizationHeader,
):
    pass


@auth_router.post(
    '/logout',
    status_code=status.HTTP_200_OK,
    summary='Инвалидировать сессию пользователя по access-токену',
    # response_model=LogoutResponseSchema,
    tags=[ApiTags.V1_AUTH],
)
async def logout(
    # access_token: AuthorizationHeader,
):
    pass
