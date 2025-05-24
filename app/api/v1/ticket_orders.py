from fastapi import APIRouter, Depends, HTTPException
from app.models.ticket_order import TicketOrderCreate, TicketOrderUpdate, TicketOrderResponse
from app.config.database import get_db
from datetime import datetime
from bson import ObjectId
from typing import List
import uuid

router = APIRouter(prefix="/ticket_orders", tags=["Ticket Orders"])

@router.post("/", response_model=TicketOrderResponse)
async def create_ticket_order(order: TicketOrderCreate, db=Depends(get_db)):
    order_dict = order.dict()
    order_dict["user_id"] = ObjectId(order_dict["user_id"])
    order_dict["event_id"] = ObjectId(order_dict["event_id"])
    order_dict["ticket_code"] = f"TICKET_{uuid.uuid4().hex[:8].upper()}"
    order_dict["payment_status"] = "pending"
    order_dict["ticket_status"] = "unused"
    order_dict["order_date"] = datetime.utcnow()
    order_dict["created_at"] = datetime.utcnow()
    order_dict["updated_at"] = datetime.utcnow()
    result = await db.ticket_orders.insert_one(order_dict)
    new_order = await db.ticket_orders.find_one({"_id": result.inserted_id})
    return TicketOrderResponse(**new_order, id=str(new_order["_id"]))

@router.get("/{order_id}", response_model=TicketOrderResponse)
async def get_ticket_order(order_id: str, db=Depends(get_db)):
    try:
        order = await db.ticket_orders.find_one({"_id": ObjectId(order_id)})
        if not order:
            raise HTTPException(status_code=404, detail="Ticket order not found")
        return TicketOrderResponse(**order, id=str(order["_id"]))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid order ID")

@router.get("/", response_model=List[TicketOrderResponse])
async def get_ticket_orders(db=Depends(get_db)):
    orders = await db.ticket_orders.find().to_list(100)
    return [TicketOrderResponse(**order, id=str(order["_id"])) for order in orders]

@router.put("/{order_id}", response_model=TicketOrderResponse)
async def update_ticket_order(order_id: str, order_update: TicketOrderUpdate, db=Depends(get_db)):
    try:
        update_dict = {k: v for k, v in order_update.dict().items() if v is not None}
        if not update_dict:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_dict["updated_at"] = datetime.utcnow()
        result = await db.ticket_orders.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": update_dict}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Ticket order not found")
        
        updated_order = await db.ticket_orders.find_one({"_id": ObjectId(order_id)})
        return TicketOrderResponse(**updated_order, id=str(updated_order["_id"]))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid order ID")

@router.delete("/{order_id}")
async def delete_ticket_order(order_id: str, db=Depends(get_db)):
    try:
        result = await db.ticket_orders.delete_one({"_id": ObjectId(order_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Ticket order not found")
        return {"message": "Ticket order deleted"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid order ID")