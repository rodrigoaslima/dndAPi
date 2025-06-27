from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.equipmentTypes import EquipmentTypes

class EquipmentTypesService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_equipment_types(self)->list[EquipmentTypes]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/equipment-categories")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No equipment found")

                equipment_types_data = data.get("results", [])
                return [EquipmentTypes.from_dict(equipment_type) for equipment_type in equipment_types_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")


    async def populate_equipment_types(self)->list[EquipmentTypes]:
        try:
            items = await self.fetch_equipment_types()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "equipment-categories",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_equipment_types(self)->list[EquipmentTypes]:
        try:
            await self.populate_equipment_types()

            collection = self.db["equipment-categories"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [EquipmentTypes.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")