from fastapi import APIRouter, Depends, HTTPException
from app.models.event import EventCreate, EventUpdate, EventResponse
from motor.motor_asyncio import AsyncIOMotorDatabase  # Updated
from app.config.database import get_db  # Updated
from datetime import datetime
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/{user_id}", response_model=EventResponse)
async def create_event(user_id: str, event: EventCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    event_dict = event.dict()
    event_dict["created_at"] = datetime.utcnow()
    event_dict["updated_at"] = datetime.utcnow()
    event_dict["organizer_id"] = user_id
    result = await db.events.insert_one(event_dict)
    new_event = await db.events.find_one({"_id": result.inserted_id})
    return EventResponse(**new_event, id=str(new_event["_id"]))

@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid event ID format")
    event = await db.events.find_one({"_id": ObjectId(event_id)})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventResponse(**event, id=str(event["_id"]))

@router.get("/", response_model=List[EventResponse])
async def get_events(db: AsyncIOMotorDatabase = Depends(get_db)):
    events = await db.events.find().to_list(100)
    return [EventResponse(**event, id=str(event["_id"])) for event in events]