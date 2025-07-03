from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.skills import Skills

class SkillsService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_skills(self)-> list[Skills]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/skills")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No skills found")

                skills_data = data.get("results", [])

                return [Skills.from_dict(skill) for skill in skills_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_skills(self)->list[Skills]:
        try:
            items = await self.fetch_skills()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "skills",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_skills(self)->list[Skills]:
        try:
            await self.populate_skills()

            collection = self.db["skills"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [Skills.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")