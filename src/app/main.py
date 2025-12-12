from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import engine
from app.db.base import Base
from app.api.v1.endpoints import assessment

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="Supply Chain Risk Monolith", lifespan=lifespan)

app.include_router(assessment.router, prefix="/api/v1/assessments", tags=["Assessments"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
