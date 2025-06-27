from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.abilityPoints import AbilityPoints

class AbilityPointsService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(db)
        self.base_url = BASE_URL

    async def fetch_ability_points(self) -> list[AbilityPoints]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/ability-scores")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No ability points found")

                ability_points_data = data.get("results", [])
                return [AbilityPoints.from_dict(ability_points) for ability_points in ability_points_data]

        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_ability_points(self)-> list[AbilityPoints]:
        try:
            items = await self.fetch_ability_points()

            await self.repo.save_items_if_not_exist(
                items=items,
                collection_name="abilityPoints",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_ability_points(self) -> list[AbilityPoints]:
        try:
           await self.populate_ability_points()

           collection = self.db["abilityPoints"]
           cursor = collection.find({})
           results = [doc async for doc in cursor]

           return [AbilityPoints.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")




