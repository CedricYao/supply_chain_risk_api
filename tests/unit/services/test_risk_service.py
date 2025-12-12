import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.risk_service import RiskAssessmentService
from app.schemas.assessment import DisruptionEvent
from app.models.shipment import ShipmentModel
from app.models.assessment import RiskAssessmentModel

@pytest.fixture
def mock_db():
    session = AsyncMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    return session

@pytest.fixture
def mock_extractor():
    extractor = MagicMock()
    extractor.parse_snippet = AsyncMock()
    return extractor

@pytest.fixture
def mock_repo():
    repo = MagicMock()
    repo.get_by_destination = AsyncMock()
    return repo

@pytest.mark.asyncio
async def test_create_assessment_empty_text(mock_db, mock_extractor, mock_repo):
    service = RiskAssessmentService(mock_db, mock_extractor, mock_repo)
    with pytest.raises(ValueError, match="News text cannot be empty"):
        await service.create_assessment("   ")

@pytest.mark.asyncio
async def test_create_assessment_disruptive(mock_db, mock_extractor, mock_repo):
    service = RiskAssessmentService(mock_db, mock_extractor, mock_repo)
    
    # Mock Event
    event = DisruptionEvent(
        target_port="Rotterdam",
        event_type="Strike",
        is_disruption=True,
        confidence_score=0.9
    )
    mock_extractor.parse_snippet.return_value = event
    
    # Mock Shipments
    shipment = ShipmentModel(id="S1", destination_port="Rotterdam", goods_description="Goods")
    mock_repo.get_by_destination.return_value = [shipment]
    
    assessment = await service.create_assessment("Strike in Rotterdam")
    
    assert assessment.detected_event["target_port"] == "Rotterdam"
    assert assessment.mitigation_strategy["action_required"] is True
    assert "Rotterdam" in assessment.mitigation_strategy["recommendation_text"]
    assert assessment.affected_shipment_ids == ["S1"]
    
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_create_assessment_non_disruptive(mock_db, mock_extractor, mock_repo):
    service = RiskAssessmentService(mock_db, mock_extractor, mock_repo)
    
    # Mock Event
    event = DisruptionEvent(
        target_port=None,
        event_type="Weather",
        is_disruption=False,
        confidence_score=0.2
    )
    mock_extractor.parse_snippet.return_value = event
    
    assessment = await service.create_assessment("Sunny weather")
    
    mock_repo.get_by_destination.assert_not_called()
    assert assessment.mitigation_strategy["action_required"] is False
    assert assessment.affected_shipment_ids == []

@pytest.mark.asyncio
async def test_create_assessment_disruptive_no_shipments(mock_db, mock_extractor, mock_repo):
    service = RiskAssessmentService(mock_db, mock_extractor, mock_repo)
    
    # Mock Event: Disruptive but no shipments will be found
    event = DisruptionEvent(
        target_port="London",
        event_type="Strike",
        is_disruption=True,
        confidence_score=0.9
    )
    mock_extractor.parse_snippet.return_value = event
    
    # Mock Shipments: Return empty list
    mock_repo.get_by_destination.return_value = []
    
    assessment = await service.create_assessment("Strike in London")
    
    # Verify interaction
    mock_repo.get_by_destination.assert_awaited_once_with("London")
    
    # Verify assessment content
    assert assessment.detected_event["target_port"] == "London"
    assert assessment.affected_shipment_ids == []
    assert assessment.mitigation_strategy["action_required"] is False
    assert "no active shipments found" in assessment.mitigation_strategy["recommendation_text"]
