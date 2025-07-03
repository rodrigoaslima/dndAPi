from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.races import Races

class RacesService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_races(self)-> list[Races]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/races")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No races found")

                races_data = data.get("results", [])

                return [Races.from_dict(race) for race in races_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_races(self)->list[Races]:
        try:
            items = await self.fetch_races()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "races",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_races(self)->list[Races]:
        try:
            await self.populate_races()

            collection = self.db["races"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [Races.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")