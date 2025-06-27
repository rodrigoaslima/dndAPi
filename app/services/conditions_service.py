from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.conditions import Conditions

class ConditionsService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_conditions(self)->list[Conditions]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/conditions")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No conditions found")

                conditions_data = data.get("results", [])
                return [Conditions.from_dict(condition) for condition in conditions_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")


    async def populate_conditions(self)->list[Conditions]:
        try:
            items = await self.fetch_conditions()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "conditions",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_conditions(self)->list[Conditions]:
        try:
            await self.populate_conditions()

            collection = self.db["conditions"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [Conditions.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")