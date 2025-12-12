from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON, Text, Uuid
from datetime import datetime, timezone
import uuid
from typing import Any, List, TYPE_CHECKING
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.shipment import ShipmentModel

class RiskAssessmentModel(Base):
    __tablename__ = "risk_assessments"

    assessment_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    
    source_snippet: Mapped[str] = mapped_column(Text, nullable=False)

    detected_event: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    mitigation_strategy: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    affected_shipment_ids: Mapped[List[str]] = mapped_column(JSON, default=list)

    # Transient field for Pydantic serialization (not persisted)
    affected_shipments: List["ShipmentModel"] = []
