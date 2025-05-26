from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Location(BaseModel):
    address: str
    city: str
    country: str
    # Bỏ trường coordinates

class TicketType(BaseModel):
    type: str
    price: float
    quantity: int
    available: int

class EventCreate(BaseModel):
    title: str
    category: str
    description: str
    start_time: str
    end_time: str
    location: Location
    ticket_types: List[TicketType]
    status: str
    organizer_id: str
    image_url: Optional[str] = None

class EventUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[Location] = None
    ticket_types: Optional[List[TicketType]] = None
    status: Optional[str] = None
    image_url: Optional[str] = None

class EventResponse(BaseModel):
    id: str
    title: str
    category: str
    description: str
    start_time: str
    end_time: str
    location: Location
    ticket_types: List[TicketType]
    status: str
    organizer_id: str
    image_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }