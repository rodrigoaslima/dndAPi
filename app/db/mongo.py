from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)

db = client["DnDataBase"]
spells_collection = db["spells"]
