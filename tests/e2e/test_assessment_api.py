import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.deps import get_risk_service
from unittest.mock import AsyncMock
from app.schemas.assessment import RiskAssessmentResponse, DisruptionEvent, MitigationAdvice
from uuid import uuid4
from datetime import datetime

@pytest.fixture
def mock_service():
    service = AsyncMock()
    return service

@pytest.mark.asyncio
async def test_create_assessment_api_success(mock_service):
    # Override dependency
    app.dependency_overrides[get_risk_service] = lambda: mock_service
    
    # Prepare mock response
    mock_response = RiskAssessmentResponse(
        assessment_id=uuid4(),
        created_at=datetime.utcnow(),
        detected_event=DisruptionEvent(
            target_port="Rotterdam", 
            event_type="Strike", 
            is_disruption=True, 
            confidence_score=0.9
        ),
        affected_shipments=[],
        mitigation_strategy=MitigationAdvice(
            recommendation_text="Avoid", 
            action_required=True
        )
    )
    mock_service.create_assessment.return_value = mock_response
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/assessments/", json={"news_text": "Strike in Rotterdam......"})
    
    assert response.status_code == 201
    data = response.json()
    assert data["detected_event"]["target_port"] == "Rotterdam"
    
    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_create_assessment_api_invalid_input(mock_service):
    app.dependency_overrides[get_risk_service] = lambda: mock_service
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/assessments/", json={"news_text": "Short"})
    
    assert response.status_code == 422
    
    app.dependency_overrides = {}
