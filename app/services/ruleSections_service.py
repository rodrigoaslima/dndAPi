from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.ruleSections import RuleSections

class RuleSectionsService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_rule_sections(self)-> list[RuleSections]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/rule-sections")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No rulesSections found")

                rule_sections_data = data.get("results", [])

                return [RuleSections.from_dict(rule) for rule in rule_sections_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_rule_sections(self)->list[RuleSections]:
        try:
            items = await self.fetch_rule_sections()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "rule-sections",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_rule_sections(self)->list[RuleSections]:
        try:
            await self.populate_rule_sections()

            collection = self.db["rule-sections"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [RuleSections.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")