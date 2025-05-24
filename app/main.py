from fastapi import FastAPI, Depends
from app.api.v1 import users, events, ticket_orders, payments
from app.config.database import get_db

app = FastAPI(title="Event Management API")

app.include_router(users.router)
app.include_router(events.router)
app.include_router(ticket_orders.router)
app.include_router(payments.router)

@app.get("/")
async def root():
    return {"message": "Event Management API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/test-db")
async def test_db(db=Depends(get_db)):
    collections = await db.list_collection_names()
    return {"collections": collections}