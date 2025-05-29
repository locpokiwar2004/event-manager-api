from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.payment import PaymentCreate, PaymentResponse
from app.config.database import get_db
from datetime import datetime, timezone
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentResponse)
async def create_payment(payment: PaymentCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    payment_dict = payment.model_dump()  # Thay dict()
    payment_dict["created_at"] = datetime.now(timezone.utc)
    payment_dict["order_id"] = str(ObjectId(payment_dict["order_id"]))
    payment_dict["user_id"] = str(ObjectId(payment_dict["user_id"]))
    result = await db.payments.insert_one(payment_dict)
    new_payment = await db.payments.find_one({"_id": result.inserted_id})
    return PaymentResponse(**new_payment, id=str(new_payment["_id"]))

@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(payment_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    if not ObjectId.is_valid(payment_id):
        raise HTTPException(status_code=400, detail="Invalid payment ID format")
    payment = await db.payments.find_one({"_id": ObjectId(payment_id)})
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return PaymentResponse(**payment, id=str(payment["_id"]))

@router.get("/", response_model=List[PaymentResponse])
async def get_payments(db: AsyncIOMotorDatabase = Depends(get_db)):
    payments = await db.payments.find().to_list(100)
    return [PaymentResponse(**payment, id=str(payment["_id"])) for payment in payments]