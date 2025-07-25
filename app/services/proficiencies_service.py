from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.proficiencies import Proficiencies

class ProficienciesService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_proficiencies(self)-> list[Proficiencies]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/proficiencies")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No proficiencies found")

                proficiencies_data = data.get("results", [])

                return [Proficiencies.from_dict(proficiency) for proficiency in proficiencies_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_proficiencies(self)->list[Proficiencies]:
        try:
            items = await self.fetch_proficiencies()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "proficiencies",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_proficiencies(self)->list[Proficiencies]:
        try:
            await self.populate_proficiencies()

            collection = self.db["proficiencies"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [Proficiencies.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")