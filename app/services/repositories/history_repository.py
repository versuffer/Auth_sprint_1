from app.core.logs import logger
from app.db.postgres.models.users import HistoryModel
from app.schemas.api.v1.auth_schemas import HistorySchemaCreate
from app.schemas.services.repositories.history_repository_schemas import HistoryDBSchema
from app.schemas.services.repositories.user_repository_schemas import UserDBSchema
from app.services.repositories.postgres_repository import PostgresRepository


class HistoryRepository:
    def __init__(self):
        self.db: PostgresRepository = PostgresRepository()

    async def get(self, user: UserDBSchema) -> list[HistoryDBSchema]:
        history = await self.db.get_all_obj(HistoryModel, where_value=[(HistoryModel.user_id, user.id)])
        return [HistoryDBSchema.model_validate(entry) for entry in history]

    async def create(self, history_data: HistorySchemaCreate) -> None:
        try:
            add_history = HistoryModel(
                user_id=history_data.user_id,
                auth_at=history_data.auth_date,
                user_agent=history_data.user_agent,
                login_type=history_data.login_type,
                session_id='53c56b98-1d6f-44fb-b7c5-082f99cb46fd',
            )
            await self.db.create_obj(add_history)
        except Exception as err:
            logger.error('Oops do not create history %s', err)
            return None
