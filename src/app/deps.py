from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.shipment_repo import ShipmentRepository
from app.services.extraction_service import IntelligentExtractionService
from app.services.risk_service import RiskAssessmentService

# Type aliases for dependency injection
DBDep = Annotated[AsyncSession, Depends(get_db)]

def get_shipment_repo(db: DBDep) -> ShipmentRepository:
    return ShipmentRepository(db)

def get_extraction_service() -> IntelligentExtractionService:
    return IntelligentExtractionService()

def get_risk_service(
    db: DBDep,
    repo: Annotated[ShipmentRepository, Depends(get_shipment_repo)],
    extractor: Annotated[IntelligentExtractionService, Depends(get_extraction_service)]
) -> RiskAssessmentService:
    return RiskAssessmentService(db, extractor, repo)
