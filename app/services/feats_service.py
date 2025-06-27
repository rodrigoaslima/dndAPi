from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.feats import Feats

class FeatsService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_feats(self)-> list[Feats]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/feats")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No feats found")

                feats_data = data.get("results", [])
                return [Feats.from_dict(feat) for feat in feats_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_feats(self)->list[Feats]:
        try:
            items = await self.fetch_feats()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "feats",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_feats(self)->list[Feats]:
        try:
            await self.populate_feats()

            collection = self.db["feats"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [Feats.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")