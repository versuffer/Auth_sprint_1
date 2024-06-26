from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.docs.tags import ApiTags
from app.exceptions import (
    AuthorizationError,
    RoleAlreadyAssignedError,
    RoleNotFoundError,
    TokenError,
    UserNotFoundError,
    auth_error,
    role_already_assigned_error,
    role_not_found_error,
    user_not_found_error,
)
from app.schemas.api.v1.roles_schemas import RoleResponseSchema
from app.services.auth.auth_service import AuthenticationService
from app.services.auth.role_services import UserRoleService
from app.services.fastapi.dependencies import get_bearer_token

users_router = APIRouter(prefix='/users')


@users_router.get(
    '/{user_id}/roles',
    status_code=status.HTTP_200_OK,
    summary='Получить все роли пользователя',
    response_model=list[RoleResponseSchema],
    tags=[ApiTags.V1_USERS],
)
async def get_user_roles(
    user_id: UUID,
    access_token: str = Depends(get_bearer_token),
    auth_service: AuthenticationService = Depends(),
    user_role_service: UserRoleService = Depends(),
):
    try:
        await auth_service.authorize_superuser(access_token=access_token)
    except (TokenError, UserNotFoundError, AuthorizationError):
        raise auth_error

    try:
        return await user_role_service.get_user_roles(user_id)
    except UserNotFoundError:
        raise user_not_found_error


@users_router.post(
    '/{user_id}/roles/{role_id}',
    status_code=status.HTTP_200_OK,
    summary='Назначить роль пользователю',
    tags=[ApiTags.V1_USERS],
)
async def assign_user_role(
    user_id: UUID,
    role_id: UUID,
    access_token: str = Depends(get_bearer_token),
    auth_service: AuthenticationService = Depends(),
    user_role_service: UserRoleService = Depends(),
):
    try:
        await auth_service.authorize_superuser(access_token=access_token)
    except (TokenError, UserNotFoundError, AuthorizationError):
        raise auth_error

    try:
        await user_role_service.assign_user_role(user_id, role_id)
        return {'detail': 'Successful assign'}
    except UserNotFoundError:
        raise user_not_found_error
    except RoleNotFoundError:
        raise role_not_found_error
    except RoleAlreadyAssignedError:
        raise role_already_assigned_error


@users_router.delete(
    '/{user_id}/roles/{role_id}',
    status_code=status.HTTP_200_OK,
    summary='Отозвать роль у пользователя',
    tags=[ApiTags.V1_USERS],
)
async def revoke_user_role(
    user_id: UUID,
    role_id: UUID,
    service: UserRoleService = Depends(),
    # access_token: AuthorizationHeader (только для суперпользователей)
):
    try:
        return await service.revoke_user_role(user_id, role_id)
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Пользователя с таким id не существует.')
    except RoleNotFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Роли с таким id не существует.')
