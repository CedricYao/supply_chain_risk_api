from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from typing import AsyncGenerator, Optional
from app.core.config import settings

class Database:
    def __init__(self) -> None:
        self._engine: Optional[AsyncEngine] = None
        self._sessionmaker: Optional[async_sessionmaker[AsyncSession]] = None

    def init(self) -> None:
        self._engine = create_async_engine(settings.DATABASE_URL, echo=False)
        self._sessionmaker = async_sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)

    @property
    def engine(self) -> AsyncEngine:
        if self._engine is None:
            self.init()
        # MyPy check: init guarantees _engine is not None
        assert self._engine is not None
        return self._engine

    @property
    def sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        if self._sessionmaker is None:
            self.init()
        assert self._sessionmaker is not None
        return self._sessionmaker

db = Database()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with db.sessionmaker() as session:
        yield session