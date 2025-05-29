from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.event import EventCreate, EventUpdate, EventResponse
from app.config.database import get_db
from datetime import datetime, timezone
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/", response_model=EventResponse)
async def create_event(event: EventCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    event_dict = event.model_dump()  # Thay dict()
    event_dict["created_at"] = datetime.now(timezone.utc)
    event_dict["updated_at"] = datetime.now(timezone.utc)
    event_dict["organizer_id"] = str(ObjectId(event_dict["organizer_id"]))
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