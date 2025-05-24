from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["event_management_db"]

async def setup_indexes():
    await db.users.create_index([("email", 1)], unique=True)
    await db.events.create_index("start_time")
    await db.events.create_index("category")
    await db.events.create_index([("location.coordinates", "2dsphere")])
    await db.ticket_orders.create_index([("ticket_code", 1)], unique=True)
    await db.ticket_orders.create_index("user_id")
    await db.ticket_orders.create_index("event_id")
    await db.payments.create_index("order_id")
    await db.payments.create_index("transaction_id")

async def get_db():
    await setup_indexes()
    return db