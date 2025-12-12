import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.extraction_service import IntelligentExtractionService, ExtractionError
from app.schemas.assessment import DisruptionEvent

@pytest.fixture
def mock_genai_client():
    client = MagicMock()
    client.aio = MagicMock()
    client.aio.models = MagicMock()
    return client

@pytest.mark.asyncio
async def test_parse_snippet_success(mock_genai_client):
    service = IntelligentExtractionService("fake_key")
    service.client = mock_genai_client
    
    # Mock response
    mock_response = MagicMock()
    mock_response.parsed = DisruptionEvent(
        target_port="Rotterdam",
        event_type="Strike",
        is_disruption=True,
        confidence_score=0.9
    )
    
    service.client.aio.models.generate_content = AsyncMock(return_value=mock_response)
    
    event = await service.parse_snippet("Some text")
    
    assert event.target_port == "Rotterdam"
    assert event.confidence_score == 0.9

@pytest.mark.asyncio
async def test_parse_snippet_failure(mock_genai_client):
    service = IntelligentExtractionService("fake_key")
    service.client = mock_genai_client
    
    # Simulate API error
    service.client.aio.models.generate_content = AsyncMock(side_effect=Exception("API Error"))
    
    with pytest.raises(ExtractionError):
        await service.parse_snippet("Some text")
