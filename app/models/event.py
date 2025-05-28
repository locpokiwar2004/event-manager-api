from pydantic import BaseModel, field_serializer
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

class EventUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[Location] = None
    ticket_types: Optional[List[TicketType]] = None
    status: Optional[str] = None
    image_url: Optional[str] = None

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
    
    @field_serializer('created_at', 'updated_at', 'start_time', 'end_time')
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat()

    class Config:
        from_attributes = True