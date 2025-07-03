from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.monsters import Monsters

class MonstersService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_monsters(self)-> list[Monsters]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/monsters")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No monsters found")

                monsters_data = data.get("results", [])

                return [Monsters.from_dict(monster) for monster in monsters_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_monsters(self)->list[Monsters]:
        try:
            items = await self.fetch_monsters()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "monsters",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_monsters(self)->list[Monsters]:
        try:
            await self.populate_monsters()

            collection = self.db["monsters"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [Monsters.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")