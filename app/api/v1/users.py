from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.user import UserCreate, UserUpdate, UserResponse
from app.config.database import get_db
from passlib.context import CryptContext
from datetime import datetime
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user_dict = user.dict()
    user_dict["password"] = pwd_context.hash(user_dict["password"])
    user_dict["created_at"] = datetime.utcnow()
    user_dict["updated_at"] = datetime.utcnow()
    result = await db.users.insert_one(user_dict)
    new_user = await db.users.find_one({"_id": result.inserted_id})
    return UserResponse(**new_user, id=str(new_user["_id"]))

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user, id=str(user["_id"]))

@router.get("/", response_model=List[UserResponse])
async def get_users(db: AsyncIOMotorDatabase = Depends(get_db)):
    users = await db.users.find().to_list(100)
    # Ensure datetime fields are handled correctly by relying on UserResponse serialization
    return [UserResponse(**user, id=str(user["_id"])) for user in users]

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    update_dict = {k: v for k, v in user_update.dict().items() if v is not None}
    if not update_dict:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    update_dict["updated_at"] = datetime.utcnow()
    result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_dict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = await db.users.find_one({"_id": ObjectId(user_id)})
    return UserResponse(**updated_user, id=str(updated_user["_id"]))

@router.delete("/{user_id}")
async def delete_user(user_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Deleted"}