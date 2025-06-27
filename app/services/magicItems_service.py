from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.magicItems import MagicItems

class MagicItemsService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_magic_items(self)-> list[MagicItems]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/magic-items")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No magic items found")

                magic_items_data = data.get("results", [])
                return [MagicItems.from_dict(magicItem) for magicItem in magic_items_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_magic_items(self)->list[MagicItems]:
        try:
            items = await self.fetch_magic_items()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "magic-items",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_magic_items(self)->list[MagicItems]:
        try:
            await self.populate_magic_items()

            collection = self.db["languages"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [MagicItems.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")