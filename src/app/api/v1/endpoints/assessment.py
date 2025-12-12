import logging
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.assessment import RiskAssessmentRequest, RiskAssessmentResponse
from app.services.risk_service import RiskAssessmentService
from app.deps import get_risk_service

router = APIRouter()

@router.post("/", response_model=RiskAssessmentResponse, status_code=status.HTTP_201_CREATED)
async def analyze_risk(
    request: RiskAssessmentRequest,
    service: Annotated[RiskAssessmentService, Depends(get_risk_service)]
):
    try:
        return await service.create_assessment(request.news_text)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        logging.error(f"Assessment failed: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
