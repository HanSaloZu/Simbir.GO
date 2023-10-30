from enum import Enum

from pydantic import BaseModel, Field


class TransportType(str, Enum):
    car = "Car"
    bike = "Bike"
    scooter = "Scooter"


class TransportUpdate(BaseModel):
    can_be_rented: bool = Field(alias="canBeRented")
    model: str
    color: str
    identifier: str
    description: str | None
    latitude: float
    longitude: float
    minute_price: float | None = Field(alias="minutePrice")
    day_price: float | None = Field(alias="dayPrice")

    class Config:
        from_attributes = True
        populate_by_name = True
