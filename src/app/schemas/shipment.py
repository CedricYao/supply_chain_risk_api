from pydantic import BaseModel, ConfigDict

class ShipmentSchema(BaseModel):
    """DTO for Shipment Entity."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    destination_port: str
    goods_description: str
