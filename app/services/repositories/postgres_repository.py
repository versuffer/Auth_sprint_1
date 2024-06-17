from typing import Any, Union

from sqlalchemy import Column, and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.postgres.base import async_engine


class PostgresRepository:
    @staticmethod
    def _build_query(
        model,
        action: Union[select, delete, update] = select,
        where_value: list[tuple[Column, Any]] | None = None,
        select_in_load: Column | None = None,
        update_values: dict | None = None,
    ):
        query = action(model)
        if where_value and len(where_value) == 1:
            _column, _value = where_value[0]
            query = query.where(_column == _value)
        if where_value and len(where_value) > 1:
            query = query.where(and_(_column == _value for _column, _value in where_value))
        if select_in_load:
            query = query.options(selectinload(select_in_load))
        if action == update:
            query = query.values(**update_values)

        return query

    async def get_one_obj(self, model, **kwargs):
        async with AsyncSession(bind=async_engine, expire_on_commit=False) as session:
            query = self._build_query(model, **kwargs)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_all_obj(self, model, **kwargs):
        async with AsyncSession(bind=async_engine, expire_on_commit=False) as session:
            query = self._build_query(model, **kwargs)
            result = await session.execute(query)
            return result.scalars().all()

    async def create_obj(self, obj) -> None:
        async with AsyncSession(bind=async_engine, expire_on_commit=False) as session:
            session.add(obj)
            await session.commit()

    async def update_obj(self, model, **kwargs) -> None:
        async with AsyncSession(bind=async_engine, expire_on_commit=False) as session:
            query = self._build_query(model, action=update, **kwargs)
            await session.execute(query)
            await session.commit()

    async def delete_obj(self, model, **kwargs) -> None:
        async with AsyncSession(bind=async_engine, expire_on_commit=False) as session:
            query = self._build_query(model, action=delete, **kwargs)
            await session.execute(query)
            await session.commit()
