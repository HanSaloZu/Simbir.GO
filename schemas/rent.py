from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class RentType(str, Enum):
    minutes = "Minutes"
    days = "Days"


class RentBase(BaseModel):
    id: int
    time_start: datetime = Field(alias="timeStart")
    time_end: datetime | None = Field(alias="timeEnd")
    type: RentType
    price_of_unit: float = Field(alias="priceOfUnit")
    final_price: float | None = Field(alias="finalPrice")
    transport_id: int = Field(alias="transportId")
    renter_id: int = Field(alias="renterId")

    class Config:
        from_attributes = True
        populate_by_name = True
