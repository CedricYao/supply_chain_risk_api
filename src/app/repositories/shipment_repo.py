from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.shipment import ShipmentModel

class ShipmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_destination(self, port_name: str) -> Sequence[ShipmentModel]:
        # Use ILIKE for case-insensitive partial matching
        # If port_name is "Port of Rotterdam", we want to match "Rotterdam"
        # If port_name is "Rotterdam", we want to match "Rotterdam"
        # A simple approach is to check if the DB value is contained in the input OR input contained in DB value.
        # But standard SQL ILIKE is usually pattern matching. 
        # Let's try matching if the DB column appears in the provided name (e.g. 'Rotterdam' in 'Port of Rotterdam')
        # OR if the provided name appears in the DB column (e.g. 'Shanghai' in 'Port of Shanghai')
        # For simplicity and the specific "Port of X" issue, checking if the DB port is IN the extracted string is robust.
        
        # However, SQLAlchemy 'in_' expects a list. 
        # Let's just stick to a simple ILIKE with wildcards around the input for now, 
        # but actually, if the AI returns "Port of Rotterdam" and DB has "Rotterdam", 
        # "Rotterdam" LIKE "%Port of Rotterdam%" is FALSE.
        # "Port of Rotterdam" LIKE "%Rotterdam%" is TRUE.
        
        # So we actually want: match if ShipmentModel.destination_port is a substring of port_name
        # OR match if port_name is a substring of ShipmentModel.destination_port
        
        # For this specific demo, let's relax it to:
        stmt = select(ShipmentModel).where(ShipmentModel.destination_port.ilike(f"%{port_name}%") | (ShipmentModel.destination_port.in_([port_name.replace("Port of ", "")])) )
        
        # Actually, simpler logic:
        # If the extracted text is "Port of Rotterdam", and we have "Rotterdam", strict equality fails.
        # We can strip "Port of " from the input `port_name` before querying.
        clean_port = port_name.replace("Port of ", "").strip()
        stmt = select(ShipmentModel).where(ShipmentModel.destination_port.ilike(f"%{clean_port}%"))

        result = await self.session.execute(stmt)
        return result.scalars().all()
