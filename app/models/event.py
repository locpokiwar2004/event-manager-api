from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict

class TicketType(BaseModel):
    type: str
    price: float
    quantity: int
    available: int

class Location(BaseModel):
    address: str
    city: str
    country: str
    coordinates: Optional[Dict]

class EventCreate(BaseModel):
    title: str
    category: str
    description: str
    start_time: datetime
    end_time: datetime
    location: Location
    ticket_types: List[TicketType]
    status: str
    organizer_id: str
    image_url: Optional[str]

class EventUpdate(BaseModel):
    title: Optional[str]
    category: Optional[str]
    description: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    location: Optional[Location]
    ticket_types: Optional[List[TicketType]]
    status: Optional[str]
    image_url: Optional[str]

class EventResponse(EventCreate):
    id: str
    created_at: str
    updated_at: str