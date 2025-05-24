from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TicketOrderCreate(BaseModel):
    user_id: str
    event_id: str
    ticket_type: str
    quantity: int
    total_amount: float

class TicketOrderUpdate(BaseModel):
    ticket_type: Optional[str]
    quantity: Optional[int]
    total_amount: Optional[float]
    payment_status: Optional[str]
    ticket_status: Optional[str]

class TicketOrderResponse(TicketOrderCreate):
    id: str
    payment_status: str
    ticket_code: str
    ticket_status: str
    order_date: str
    created_at: str
    updated_at: str