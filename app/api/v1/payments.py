from fastapi import APIRouter, Depends, HTTPException
from app.models.payment import PaymentCreate, PaymentUpdate, PaymentResponse
from app.config.database import get_db
from datetime import datetime
from bson import ObjectId
from typing import List
import uuid

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentResponse)
async def create_payment(payment: PaymentCreate, db=Depends(get_db)):
    order = await db.ticket_orders.find_one({"_id": ObjectId(payment.order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Ticket order not found")

    payment_dict = payment.dict()
    payment_dict["order_id"] = ObjectId(payment_dict["order_id"])
    payment_dict["user_id"] = ObjectId(payment_dict["user_id"])
    payment_dict["transaction_id"] = f"TXN_{uuid.uuid4().hex[:8].upper()}"
    payment_dict["status"] = "pending"
    payment_dict["created_at"] = datetime.utcnow()
    result = await db.payments.insert_one(payment_dict)
    new_payment = await db.payments.find_one({"_id": result.inserted_id})

    await db.ticket_orders.update_one(
        {"_id": ObjectId(payment.order_id)},
        {"$set": {"payment_status": "pending"}}
    )

    return PaymentResponse(**new_payment, id=str(new_payment["_id"]))

@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(payment_id: str, db=Depends(get_db)):
    try:
        payment = await db.payments.find_one({"_id": ObjectId(payment_id)})
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return PaymentResponse(**payment, id=str(payment["_id"]))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payment ID")

@router.get("/", response_model=List[PaymentResponse])
async def get_payments(db=Depends(get_db)):
    payments = await db.payments.find().to_list(100)
    return [PaymentResponse(**payment, id=str(payment["_id"])) for payment in payments]

@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment(payment_id: str, payment_update: PaymentUpdate, db=Depends(get_db)):
    try:
        update_dict = {k: v for k, v in payment_update.dict().items() if v is not None}
        if not update_dict:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_dict["updated_at"] = datetime.utcnow()
        result = await db.payments.update_one(
            {"_id": ObjectId(payment_id)},
            {"$set": update_dict}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        updated_payment = await db.payments.find_one({"_id": ObjectId(payment_id)})
        return PaymentResponse(**updated_payment, id=str(updated_payment["_id"]))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payment ID")

@router.delete("/{payment_id}")
async def delete_payment(payment_id: str, db=Depends(get_db)):
    try:
        result = await db.payments.delete_one({"_id": ObjectId(payment_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Payment not found")
        return {"message": "Payment deleted"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payment ID")