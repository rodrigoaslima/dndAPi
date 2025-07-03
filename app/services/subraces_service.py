from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.subraces import Subraces

class SubracesService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_subraces(self)-> list[Subraces]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/subraces")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No subraces found")

                subraces_data = data.get("results", [])

                return [Subraces.from_dict(subrace) for subrace in subraces_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_subraces(self)->list[Subraces]:
        try:
            items = await self.fetch_subraces()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "subraces",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_subraces(self)->list[Subraces]:
        try:
            await self.populate_subraces()

            collection = self.db["subraces"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [Subraces.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")