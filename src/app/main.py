import yaml
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import db
from app.db.base import Base
from app.api.v1.endpoints import assessment
from app.models.shipment import ShipmentModel
from sqlalchemy import select

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed data
    try:
        with open("seed_data.yaml", "r") as f:
            data = yaml.safe_load(f)
            if data and "shipments" in data:
                async with db.sessionmaker() as session:
                    # Check if data already exists to avoid duplicates on reload (though in-memory wipes anyway)
                    result = await session.execute(select(ShipmentModel).limit(1))
                    if not result.scalar():
                        shipments = [ShipmentModel(**item) for item in data["shipments"]]
                        session.add_all(shipments)
                        await session.commit()
                        print(f"Seeded {len(shipments)} shipments from seed_data.yaml")
    except FileNotFoundError:
        print("seed_data.yaml not found, skipping seeding.")
    except Exception as e:
        print(f"Failed to seed data: {e}")

    yield
    await db.engine.dispose()

app = FastAPI(title="Supply Chain Risk Monolith", lifespan=lifespan)

app.include_router(assessment.router, prefix="/api/v1/assessments", tags=["Assessments"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
