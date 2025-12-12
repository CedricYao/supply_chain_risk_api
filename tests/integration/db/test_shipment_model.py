import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.models.shipment import ShipmentModel
from app.db.base import Base
from sqlalchemy import select

# Use in-memory SQLite for tests
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

@pytest.mark.asyncio
async def test_shipment_persistence(db_session):
    shipment = ShipmentModel(
        id="SCH-9001",
        destination_port="Rotterdam",
        goods_description="Bananas"
    )
    db_session.add(shipment)
    await db_session.commit()
    await db_session.refresh(shipment)

    assert shipment.id == "SCH-9001"
    
    # Retrieve
    result = await db_session.execute(select(ShipmentModel).where(ShipmentModel.id == "SCH-9001"))
    retrieved = result.scalar_one()
    
    assert retrieved.destination_port == "Rotterdam"
    assert retrieved.goods_description == "Bananas"
