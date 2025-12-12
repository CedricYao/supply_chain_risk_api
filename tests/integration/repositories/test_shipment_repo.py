import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.models.shipment import ShipmentModel
from app.repositories.shipment_repo import ShipmentRepository
from app.db.base import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with SessionLocal() as session:
        yield session
    
    await engine.dispose()

@pytest.fixture
async def seeded_session(db_session):
    shipments = [
        ShipmentModel(id="S1", destination_port="Rotterdam", goods_description="A"),
        ShipmentModel(id="S2", destination_port="Rotterdam", goods_description="B"),
        ShipmentModel(id="S3", destination_port="Hamburg", goods_description="C"),
    ]
    db_session.add_all(shipments)
    await db_session.commit()
    return db_session

@pytest.mark.asyncio
async def test_get_by_destination(seeded_session):
    repo = ShipmentRepository(seeded_session)
    
    # Match
    results = await repo.get_by_destination("Rotterdam")
    assert len(results) == 2
    assert set(s.id for s in results) == {"S1", "S2"}
    
    # No match
    results_empty = await repo.get_by_destination("Unknown")
    assert len(results_empty) == 0
