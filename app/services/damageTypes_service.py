from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.damageTypes import DamageTypes

class DamageTypesService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_damage_types(self)->list[DamageTypes]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/damage-types")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No damageTypes found")

                damage_types_data = data.get("results", [])
                return [DamageTypes.from_dict(damageType) for damageType in damage_types_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")


    async def populate_damage_types(self)->list[DamageTypes]:
        try:
            items = await self.fetch_damage_types()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "damageTypes",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_damage_types(self)->list[DamageTypes]:
        try:
            await self.populate_damage_types()

            collection = self.db["damageTypes"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [DamageTypes.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")