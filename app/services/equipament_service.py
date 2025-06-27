from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.equipament import Equipment

class EquipmentService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_equipment(self)->list[Equipment]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/equipment")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No equipment found")

                equipment_data = data.get("results", [])
                return [Equipment.from_dict(equipment) for equipment in equipment_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")


    async def populate_equipment(self)->list[Equipment]:
        try:
            items = await self.fetch_equipment()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "equipment",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_equipment(self)->list[Equipment]:
        try:
            await self.populate_equipment()

            collection = self.db["equipment"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [Equipment.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")