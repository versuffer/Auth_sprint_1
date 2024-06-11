from uuid import UUID

from fastapi import APIRouter, status

from app.api.docs.tags import ApiTags

users_router = APIRouter(prefix='/users')


@users_router.get(
    '/{user_id}/roles',
    status_code=status.HTTP_200_OK,
    summary='Получить все роли пользователя',
    # response_model=GetUserRolesResponseSchema,
    tags=[ApiTags.V1_USERS],
)
async def get_user_roles(
    user_id: UUID,
    # access_token: AuthorizationHeader (только для суперпользователей)
):
    pass


@users_router.post(
    '/{user_id}/roles/{role_id}',
    status_code=status.HTTP_200_OK,
    summary='Назначить роль пользователю',
    # response_model=AssignUserRoleResponseSchema,
    tags=[ApiTags.V1_USERS],
)
async def assign_user_role(
    user_id: UUID,
    role_id: UUID,
    # access_token: AuthorizationHeader (только для суперпользователей)
):
    pass


@users_router.delete(
    '/{user_id}/roles/{role_id}',
    status_code=status.HTTP_200_OK,
    summary='Отозвать роль у пользователя',
    # response_model=RevokeUserRoleResponseSchema,
    tags=[ApiTags.V1_USERS],
)
async def revoke_user_role(
    user_id: UUID,
    role_id: UUID,
    # access_token: AuthorizationHeader (только для суперпользователей)
):
    pass
