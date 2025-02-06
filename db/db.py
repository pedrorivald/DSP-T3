from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017/oficina"
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database()