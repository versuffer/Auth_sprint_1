import pytest
from fastapi import status
from httpx import AsyncClient

from app.main import app
from app.schemas.api.v1.auth_schemas import TokenPairSchema, UserCredentialsSchema
from app.schemas.services.auth.user_service_schemas import UserSchema


@pytest.mark.anyio
class TestLogin:
    async def test_login_by_username_200(
        self, async_test_client: AsyncClient, test_user_data: dict, registered_user: UserSchema
    ):
        # Arrange
        user_credentials = UserCredentialsSchema(login=registered_user.username, password=test_user_data['password'])
        user_credentials_json = user_credentials.model_dump(mode='json')
        user_agent = 'random_user_agent_info'

        # Act
        response = await async_test_client.post(
            app.url_path_for('api_v1_login'), json=user_credentials_json, headers={'User-Agent': user_agent}
        )
        response_json = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response_json == TokenPairSchema(**response_json).model_dump(mode='json')
