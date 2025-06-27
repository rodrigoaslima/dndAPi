import httpx
from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.spell import Spell

class SpellsService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_spells(self)-> list[Spell]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/spells")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No spells found")

                spell_data = data.get("results", [])
                return [Spell.from_dict(spell) for spell in spell_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_spells(self)->list[Spell]:
        try:
            items = await self.fetch_spells()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "spells",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_spells(self)->list[Spell]:
        try:
            await self.populate_spells()

            collection = self.db["spells"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [Spell.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")