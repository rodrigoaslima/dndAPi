from motor.motor_asyncio import AsyncIOMotorCursor
from typing import Any

class MongoRepository:
    def __init__(self, db: AsyncIOMotorCursor):
        self.db = db

    async def save_items_if_not_exist(self, items: list[Any], collection_name: str, unique_field: str = "index") -> int:
        collection = self.db[collection_name]

        existing_docs = collection.find({}, {unique_field: 1, "_id": 0})
        existing_values = {
            doc[unique_field]
            async for doc in existing_docs
        }

        new_items = [
            item.to_dict()
            for item in items
            if getattr(item, unique_field) not in existing_values
        ]

        if new_items:
            result = await collection.insert_many(new_items)
            return len(result.inserted_ids)

        return 0