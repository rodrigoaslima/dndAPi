from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.rules import Rules

class RulesService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_rules(self)-> list[Rules]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/rules")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No rules found")

                rules_data = data.get("results", [])

                return [Rules.from_dict(rule) for rule in rules_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_rules(self)->list[Rules]:
        try:
            items = await self.fetch_rules()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "rules",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_rules(self)->list[Rules]:
        try:
            await self.populate_rules()

            collection = self.db["rules"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [Rules.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")