from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentCreate(BaseModel):
    order_id: str
    user_id: str
    payment_method: str
    transaction_id: str
    status: str
    amount: Optional[float] = None
    payment_link: Optional[str] = None

class PaymentResponse(BaseModel):
    id: str
    order_id: str
    user_id: str
    payment_method: str
    transaction_id: str
    status: str
    amount: Optional[float] = None
    payment_link: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True