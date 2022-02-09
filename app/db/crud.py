from abc import ABC
from contextlib import asynccontextmanager
from typing import (
    TypeVar,
    ClassVar,
    Type,
    Any,
    Optional,
    cast,
    List,
    AsyncContextManager, Union
)

from sqlalchemy import select, update, exists, delete, func, lambda_stmt
from sqlalchemy.ext.asyncio import AsyncSessionTransaction, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import Executable

Model = TypeVar("Model")
TransactionContext = AsyncContextManager[AsyncSessionTransaction]


class BaseCRUD(ABC):

    def __init__(
            self,
            db_session: Union[sessionmaker, AsyncSession],
            model: ClassVar[Type[Model]]
    ):
        self.model = model

        if isinstance(db_session, sessionmaker):
            self.session: AsyncSession = cast(AsyncSession, db_session())
        else:
            self.session = db_session

    @asynccontextmanager
    async def transaction(self) -> TransactionContext:
        async with self.session as transaction:
            yield transaction

    async def insert(self, **kwargs: Any) -> Model:
        add_model = self._convert_to_model(**kwargs)
        self.session.add(add_model)
        await self.session.commit()
        return add_model

    async def get_one(self, *args) -> Model:
        async with self.session as transaction:
            stmt = select(self.model).where(*args)
            result = await self.session.execute(stmt)
            return result.scalar_one()

    async def get_many(self, *args: Any) -> Model:
        query_model = self.model
        stmt = lambda_stmt(lambda: select(query_model))
        stmt += lambda s: s.where(*args)
        query_stmt = cast(Executable, stmt)

        result = await self.session.execute(query_stmt)
        return result.scalars().all()

    async def update(self, *args: Any, **kwargs: Any) -> Model:
        stmt = (
            update(self.model)
            .where(*args)
            .values(**kwargs)
            .returning(self.model)
        )

        stmt = (
            select(self.model)
            .from_statement(stmt)
            .execution_options(synchronize_session="fetch")
        )

        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def exists(self, *args: Any) -> Optional[bool]:
        """Check is row exists in database"""
        stmt = exists(select(self.model).where(*args)).select()
        result_stmt = await self.session.execute(stmt)
        result = result_stmt.scalar()
        return cast(Optional[bool], result)

    async def exists_get(self, *args: Any) -> List[Model]:
        """Check is row exists in database. If it does, returns the row"""
        stmt = select(self.model).where(*args)
        result_stmt = await self.session.execute(stmt)
        result = result_stmt.scalars().all()
        return result

    async def delete(self, *args: Any) -> List[Model]:
        stmt = delete(self.model).where(*args).returning("*")
        result = await self.session.execute(stmt)
        await self.session.commit()
        result_all = result.scalars().all()
        return result_all

    async def soft_delete(self, *args: Any) -> List[Model]:
        return await self.update(*args, status_id=0)

    async def count(self) -> int:
        stmt = select(func.count()).select_from(select(self.model).subquery())
        result = await self.session.execute(stmt)
        count = result.scalar_one()
        return cast(int, count)

    def _convert_to_model(self, **kwargs) -> Model:
        return self.model(**kwargs)  # type: ignore
