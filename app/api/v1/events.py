from fastapi import APIRouter, Depends, HTTPException
from app.models.event import EventCreate, EventUpdate, EventResponse
from app.config.database import get_db
from datetime import datetime
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/", response_model=EventResponse)
async def create_event(event: EventCreate, db=Depends(get_db)):
    try:
        # Kiểm tra organizer_id hợp lệ
        if not ObjectId.is_valid(event.organizer_id):
            raise HTTPException(status_code=400, detail="Invalid organizer ID")
        
        event_dict = event.dict()
        event_dict["organizer_id"] = ObjectId(event_dict["organizer_id"])
        event_dict["created_at"] = datetime.utcnow()
        event_dict["updated_at"] = datetime.utcnow()
        result = await db.events.insert_one(event_dict)
        new_event = await db.events.find_one({"_id": result.inserted_id})
        return EventResponse(**new_event, id=str(new_event["_id"]))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid organizer ID")

@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: str, db=Depends(get_db)):
    try:
        event = await db.events.find_one({"_id": ObjectId(event_id)})
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return EventResponse(**event, id=str(event["_id"]))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid event ID")

@router.get("/", response_model=List[EventResponse])
async def get_events(db=Depends(get_db)):
    events = await db.events.find().to_list(100)
    return [EventResponse(**event, id=str(event["_id"])) for event in events]

@router.put("/{event_id}", response_model=EventResponse)
async def update_event(event_id: str, event_update: EventUpdate, db=Depends(get_db)):
    try:
        update_dict = {k: v for k, v in event_update.dict(exclude_unset=True).items() if v is not None}
        if not update_dict:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_dict["updated_at"] = datetime.utcnow()
        result = await db.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$set": update_dict}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Event not found")
        
        updated_event = await db.events.find_one({"_id": ObjectId(event_id)})
        return EventResponse(**updated_event, id=str(updated_event["_id"]))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid event ID")

@router.delete("/{event_id}")
async def delete_event(event_id: str, db=Depends(get_db)):
    try:
        result = await db.events.delete_one({"_id": ObjectId(event_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Event not found")
        return {"message": "Event deleted"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid event ID")