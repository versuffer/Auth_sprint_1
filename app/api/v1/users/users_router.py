from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.docs.tags import ApiTags
from app.exceptions import RoleAlreadyExistError, RoleNotFoundError, UserNotFoundError
from app.schemas.api.v1.roles_schemas import (
    AssignUserRoleResponseSchema,
    GetUserRolesResponseSchema,
    RevokeUserRoleResponseSchema,
)
from app.services.auth.role_services import UserRoleService

users_router = APIRouter(prefix='/users')


@users_router.get(
    '/{user_id}/roles',
    status_code=status.HTTP_200_OK,
    summary='Получить все роли пользователя',
    response_model=GetUserRolesResponseSchema,
    tags=[ApiTags.V1_USERS],
)
async def get_user_roles(
    user_id: UUID,
    service: UserRoleService = Depends(),
    # access_token: AuthorizationHeader (только для суперпользователей)
):
    try:
        return await service.get_user_roles(user_id)
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Пользователя с таким id не существует.')


@users_router.post(
    '/{user_id}/roles/{role_id}',
    status_code=status.HTTP_200_OK,
    summary='Назначить роль пользователю',
    response_model=AssignUserRoleResponseSchema,
    tags=[ApiTags.V1_USERS],
)
async def assign_user_role(
    user_id: UUID,
    role_id: UUID,
    service: UserRoleService = Depends(),
    # access_token: AuthorizationHeader (только для суперпользователей)
):
    try:
        return await service.assign_user_role(user_id, role_id)
    except RoleAlreadyExistError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пользователи уже имеет эту роль')
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Пользователя с таким id не существует.')
    except RoleNotFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Роли с таким id не существует.')


@users_router.delete(
    '/{user_id}/roles/{role_id}',
    status_code=status.HTTP_200_OK,
    summary='Отозвать роль у пользователя',
    response_model=RevokeUserRoleResponseSchema,
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
