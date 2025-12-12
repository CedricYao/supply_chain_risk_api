from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.shipment import ShipmentModel

class ShipmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_destination(self, port_name: str) -> Sequence[ShipmentModel]:
        stmt = select(ShipmentModel).where(ShipmentModel.destination_port == port_name)
        result = await self.session.execute(stmt)
        return result.scalars().all()
