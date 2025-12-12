import pytest
from pydantic import ValidationError
from app.schemas.assessment import DisruptionEvent, RiskAssessmentRequest, MitigationAdvice, RiskAssessmentResponse
from datetime import datetime
from uuid import uuid4

def test_disruption_event_confidence_score_validation():
    # Valid
    DisruptionEvent(
        target_port="Rotterdam",
        event_type="Strike",
        is_disruption=True,
        confidence_score=0.5
    )
    
    # Invalid < 0
    with pytest.raises(ValidationError) as excinfo:
        DisruptionEvent(
            target_port="Rotterdam",
            event_type="Strike",
            is_disruption=True,
            confidence_score=-0.1
        )
    assert "Input should be greater than or equal to 0" in str(excinfo.value)
    
    # Invalid > 1
    with pytest.raises(ValidationError) as excinfo:
        DisruptionEvent(
            target_port="Rotterdam",
            event_type="Strike",
            is_disruption=True,
            confidence_score=1.1
        )
    assert "Input should be less than or equal to 1" in str(excinfo.value)

def test_risk_assessment_request_validation():
    # Valid
    RiskAssessmentRequest(news_text="This is a long enough news snippet regarding a port strike.")
    
    # Invalid: too short
    with pytest.raises(ValidationError) as excinfo:
        RiskAssessmentRequest(news_text="Short")
    assert "String should have at least 10 characters" in str(excinfo.value)

def test_disruption_event_is_unknown():
    event = DisruptionEvent(
        target_port=None,
        event_type="Unknown",
        is_disruption=False,
        confidence_score=0.0
    )
    assert event.is_unknown() is True

    event_known = DisruptionEvent(
        target_port="Hamburg",
        event_type="Strike",
        is_disruption=True,
        confidence_score=0.9
    )
    assert event_known.is_unknown() is False
