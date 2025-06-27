from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.features import Features

class FeaturesService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_features(self)-> list[Features]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/features")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No features found")

                feature_data = data.get("results", [])
                return [Features.from_dict(feature) for feature in feature_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_features(self)->list[Features]:
        try:
            items = await self.fetch_features()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "features",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_features(self)->list[Features]:
        try:
            await self.populate_features()

            collection = self.db["features"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [Features.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")