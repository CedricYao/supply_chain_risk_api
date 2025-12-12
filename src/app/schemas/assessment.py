from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.schemas.shipment import ShipmentSchema

class DisruptionEvent(BaseModel):
    """Value Object representing the AI-extracted event."""
    model_config = ConfigDict(strict=True, frozen=True)

    target_port: Optional[str] = Field(
        None, description="The port identified in the text. None if unknown."
    )
    event_type: str = Field(..., description="Type of event (e.g., 'Strike', 'Weather').")
    is_disruption: bool = Field(..., description="True if the event negatively impacts operations.")
    confidence_score: float = Field(..., ge=0.0, le=1.0)

    def is_unknown(self) -> bool:
        return self.target_port is None

class MitigationAdvice(BaseModel):
    """Value Object for generated advice."""
    model_config = ConfigDict(strict=True, frozen=True)

    recommendation_text: str
    action_required: bool

class RiskAssessmentRequest(BaseModel):
    """Input payload for the API."""
    news_text: str = Field(..., min_length=10, description="Raw news snippet to analyze.")

class RiskAssessmentResponse(BaseModel):
    """Aggregate Response DTO."""
    model_config = ConfigDict(from_attributes=True)

    assessment_id: UUID
    created_at: datetime
    detected_event: DisruptionEvent
    affected_shipments: List[ShipmentSchema]
    mitigation_strategy: MitigationAdvice
