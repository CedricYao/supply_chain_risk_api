import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.models.assessment import RiskAssessmentModel
from app.db.base import Base
from sqlalchemy import select
from uuid import uuid4

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
async def test_assessment_persistence(db_session):
    event_data = {
        "target_port": "Rotterdam",
        "event_type": "Strike",
        "is_disruption": True,
        "confidence_score": 0.95
    }
    
    assessment = RiskAssessmentModel(
        source_snippet="Strike in Rotterdam",
        detected_event=event_data,
        mitigation_strategy={"action_required": True, "recommendation_text": "Avoid"},
        affected_shipment_ids=["SCH-123"]
    )
    
    db_session.add(assessment)
    await db_session.commit()
    await db_session.refresh(assessment)
    
    assert assessment.assessment_id is not None
    
    # Retrieve
    result = await db_session.execute(select(RiskAssessmentModel).where(RiskAssessmentModel.assessment_id == assessment.assessment_id))
    retrieved = result.scalar_one()
    
    assert retrieved.detected_event["target_port"] == "Rotterdam"
    assert retrieved.affected_shipment_ids == ["SCH-123"]
