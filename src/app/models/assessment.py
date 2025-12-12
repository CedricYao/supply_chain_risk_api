from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON, Text, Uuid
from datetime import datetime
import uuid
from typing import Any, List
from app.db.base import Base

class RiskAssessmentModel(Base):
    __tablename__ = "risk_assessments"

    assessment_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    source_snippet: Mapped[str] = mapped_column(Text, nullable=False)

    detected_event: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    mitigation_strategy: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    affected_shipment_ids: Mapped[List[str]] = mapped_column(JSON, default=list)
