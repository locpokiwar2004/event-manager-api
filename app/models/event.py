from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Coordinates(BaseModel):
    lat: Optional[float] = None
    lng: Optional[float] = None

class Location(BaseModel):
    address: str
    city: str
    country: str
    coordinates: Optional[Coordinates] = None

class TicketType(BaseModel):
    type: str
    price: float
    quantity: int
    available: int

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
    image_url: str

class EventResponse(BaseModel):
    id: str
    title: str
    category: str
    description: str
    start_time: datetime
    end_time: datetime
    location: Location
    ticket_types: List[TicketType]
    status: str
    organizer_id: str
    image_url: str
    created_at: datetime 
    updated_at: datetime  
    class Config:
        from_attributes = True