from pydantic import BaseModel
from typing import Optional, Dict

class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    address: Dict
    role: Optional[str] = "customer"

class UserUpdate(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    address: Optional[Dict]
    role: Optional[str]

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    address: Dict
    role: str
    created_at: str
    updated_at: str