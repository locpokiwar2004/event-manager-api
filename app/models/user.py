from pydantic import BaseModel
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

    class Config:
        from_attributes = True