from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import TEXT
from app.db.base import Base

class ShipmentModel(Base):
    __tablename__ = "shipments"

    id: Mapped[str] = mapped_column(TEXT, primary_key=True)
    destination_port: Mapped[str] = mapped_column(TEXT, index=True, nullable=False)
    goods_description: Mapped[str] = mapped_column(TEXT, nullable=False)
