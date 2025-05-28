from pydantic import BaseModel, field_serializer
from typing import Optional
from datetime import datetime

class Address(BaseModel):
    street: str
    city: str
    country: str

class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    address: Address
    role: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[Address] = None
    role: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    password: Optional[str] = None
    address: Address
    role: str
    created_at: datetime
    updated_at: datetime

    @field_serializer('created_at', 'updated_at')
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat()  # Convert datetime to ISO 8601 string

    class Config:
        from_attributes = True