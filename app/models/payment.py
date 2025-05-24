from pydantic import BaseModel
from typing import Optional

class PaymentCreate(BaseModel):
    order_id: str
    user_id: str
    amount: float

class PaymentUpdate(BaseModel):
    status: Optional[str]
    transaction_id: Optional[str]
    payment_link: Optional[str]

class PaymentResponse(PaymentCreate):
    id: str
    payment_method: str
    transaction_id: str
    status: str
    payment_link: str
    created_at: str