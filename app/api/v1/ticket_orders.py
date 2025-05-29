from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.ticket_order import TicketOrderCreate, TicketOrderResponse
from app.config.database import get_db
from datetime import datetime, timezone
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/ticket_orders", tags=["Ticket Orders"])

@router.post("/", response_model=TicketOrderResponse)
async def create_ticket_order(order: TicketOrderCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    order_dict = order.model_dump()  # Thay dict()
    order_dict["order_date"] = datetime.now(timezone.utc)
    order_dict["created_at"] = datetime.now(timezone.utc)
    order_dict["updated_at"] = datetime.now(timezone.utc)
    order_dict["user_id"] = str(ObjectId(order_dict["user_id"]))
    order_dict["event_id"] = str(ObjectId(order_dict["event_id"]))
    result = await db.ticket_orders.insert_one(order_dict)
    new_order = await db.ticket_orders.find_one({"_id": result.inserted_id})
    return TicketOrderResponse(**new_order, id=str(new_order["_id"]))

@router.get("/{order_id}", response_model=TicketOrderResponse)
async def get_ticket_order(order_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid order ID format")
    order = await db.ticket_orders.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Ticket order not found")
    return TicketOrderResponse(**order, id=str(order["_id"]))

@router.get("/", response_model=List[TicketOrderResponse])
async def get_ticket_orders(db: AsyncIOMotorDatabase = Depends(get_db)):
    orders = await db.ticket_orders.find().to_list(100)
    return [TicketOrderResponse(**order, id=str(order["_id"])) for order in orders]