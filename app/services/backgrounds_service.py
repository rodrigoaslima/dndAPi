from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.background import Background

class BackgroundService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(db)
        self.base_url = BASE_URL

    async def fetch_backgrounds(self)->list[Background]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/backgrounds")
                response.raise_for_status()
                data = response.json()
                if not data:
                    raise HTTPException(status_code=500, detail="No background found")

                backgrounds_data = data.get("results", [])
                return [Background.from_dict(background) for background in backgrounds_data]
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_backgrounds(self)->list[Background]:
        try:
            items = await self.fetch_backgrounds()

            await self.repo.save_items_if_not_exist(
                items=items,
                collection_name="backgrounds",
                unique_field="index"
            )
            return items
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_backgrounds(self)->list[Background]:
        try:
            await self.populate_backgrounds()

            collection = self.db["backgrounds"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [Background.from_dict(doc) for doc in results]
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Error in getting alignments: {str(e)}")

