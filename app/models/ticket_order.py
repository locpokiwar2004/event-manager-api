from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketOrderCreate(BaseModel):
    user_id: str
    event_id: str
    ticket_type: str
    quantity: int
    total_amount: float
    payment_status: str
    ticket_code: str
    ticket_status: str

class TicketOrderResponse(BaseModel):
    id: str
    user_id: str
    event_id: str
    ticket_type: str
    quantity: int
    total_amount: float
    payment_status: str
    ticket_code: str
    ticket_status: str
    order_date: datetime  # Sửa thành datetime
    created_at: datetime  # Sửa thành datetime
    updated_at: datetime  # Sửa thành datetime

    class Config:
        from_attributes = True