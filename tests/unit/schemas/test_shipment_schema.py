import pytest
from pydantic import ValidationError
from app.schemas.shipment import ShipmentSchema

def test_shipment_schema_valid():
    data = {
        "id": "SCH-123",
        "destination_port": "Rotterdam",
        "goods_description": "Bananas"
    }
    shipment = ShipmentSchema(**data)
    assert shipment.id == "SCH-123"
    assert shipment.destination_port == "Rotterdam"
    assert shipment.goods_description == "Bananas"

def test_shipment_schema_missing_destination():
    data = {
        "id": "SCH-123",
        "goods_description": "Bananas"
    }
    with pytest.raises(ValidationError) as excinfo:
        ShipmentSchema(**data)
    
    assert "destination_port" in str(excinfo.value)
    assert "Field required" in str(excinfo.value)
