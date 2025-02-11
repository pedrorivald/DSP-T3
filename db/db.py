import os
from motor.motor_asyncio import AsyncIOMotorClient

host = os.getenv("MONGO_HOST", "oficina-mongodb")

MONGO_URI = f"mongodb://{host}:27017/oficina"
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database()