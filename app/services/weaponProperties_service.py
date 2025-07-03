from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.weaponProperties import WeaponProperties

class WeaponPropertiesService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_weapon_properties(self)-> list[WeaponProperties]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/weapon-properties")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No fetch_weapon_properties found")

                fetch_weapon_properties_data = data.get("results", [])

                return [WeaponProperties.from_dict(weapon) for weapon in fetch_weapon_properties_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_fetch_weapon_properties(self)->list[WeaponProperties]:
        try:
            items = await self.fetch_weapon_properties()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "weapon-properties",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_weapon_properties(self)->list[WeaponProperties]:
        try:
            await self.populate_fetch_weapon_properties()

            collection = self.db["weapon-properties"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [WeaponProperties.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")