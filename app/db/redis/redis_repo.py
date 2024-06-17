import uuid

import redis.asyncio as redis


class RedisRepository:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis = redis.from_url(self.redis_url)
        self.expire_time: int = 60

    async def save_session(self, login: str, session_id: uuid.UUID) -> None:
        session_key = f'session:{session_id}'
        await self.redis.set(session_key, login, ex=self.expire_time)

    async def delete_session(self, session_id: uuid.UUID) -> None:
        session_key = f'session:{session_id}'
        await self.redis.delete(session_key)
