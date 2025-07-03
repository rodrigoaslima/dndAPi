from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.traits import Traits

class TraitsService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_traits(self)-> list[Traits]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/traits")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No traits found")

                traits_data = data.get("results", [])

                return [Traits.from_dict(trait) for trait in traits_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_traits(self)->list[Traits]:
        try:
            items = await self.fetch_traits()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "traits",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_traits(self)->list[Traits]:
        try:
            await self.populate_traits()

            collection = self.db["traits"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [Traits.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")