from pydantic import BaseModel, Field
from typing import Literal

class BookingCreate(BaseModel):
    booking_type: Literal["bus", "flight", "cinema"]
    item_id: int
    seats: list[str] = Field(min_length=1, max_length=10)

class BookingOut(BaseModel):
    id: int
    pnr: str
    booking_type: str
    item_id: int
    seats: list[str]
    amount: float
    status: str
    payment_status: str
    model_config = {"from_attributes": True}
