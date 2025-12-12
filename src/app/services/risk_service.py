from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.assessment import RiskAssessmentModel
from app.models.shipment import ShipmentModel
from app.repositories.shipment_repo import ShipmentRepository
from app.services.extraction_service import IntelligentExtractionService
from app.schemas.assessment import DisruptionEvent, MitigationAdvice

class RiskAssessmentService:
    def __init__(
        self, 
        db: AsyncSession, 
        extractor: IntelligentExtractionService,
        shipment_repo: ShipmentRepository
    ):
        self.db = db
        self.extractor = extractor
        self.shipment_repo = shipment_repo

    async def create_assessment(self, news_text: str) -> RiskAssessmentModel:
        # 1. Validation (BR-001)
        if not news_text.strip():
            raise ValueError("News text cannot be empty")

        # 2. Extract Event (BR-002, BR-003, BR-004)
        event: DisruptionEvent = await self.extractor.parse_snippet(news_text)

        # 3. Identify Impact (BR-005)
        affected_shipments: Sequence[ShipmentModel] = []
        if not event.is_unknown() and event.is_disruption:
            assert event.target_port is not None
            affected_shipments = await self.shipment_repo.get_by_destination(event.target_port)

        # 4. Formulate Strategy (BR-006, BR-007)
        strategy = self._generate_strategy(event, affected_shipments)

        # 5. Persist Aggregate
        assessment = RiskAssessmentModel(
            source_snippet=news_text,
            detected_event=event.model_dump(),
            mitigation_strategy=strategy.model_dump(),
            affected_shipment_ids=[s.id for s in affected_shipments]
        )
        self.db.add(assessment)
        await self.db.commit()
        await self.db.refresh(assessment)
        
        return assessment

    def _generate_strategy(self, event: DisruptionEvent, shipments: Sequence[ShipmentModel]) -> MitigationAdvice:
        if not event.is_disruption:
            return MitigationAdvice(
                recommendation_text="No action required. Event is non-disruptive.",
                action_required=False
            )
        
        if not shipments:
             return MitigationAdvice(
                recommendation_text=f"Disruption at {event.target_port}, but no active shipments found.",
                action_required=False 
            )

        return MitigationAdvice(
            recommendation_text=f"Action Required: Reroute {len(shipments)} shipments destined for {event.target_port} due to {event.event_type}.",
            action_required=True
        )
