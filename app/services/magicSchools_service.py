from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.magicSchools import MagicSchools

class MagicSchoolsService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_magic_schools(self)-> list[MagicSchools]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/magic-schools")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No magic schools found")

                magic_schools_data = data.get("results", [])

                return [MagicSchools.from_dict(magicSchool) for magicSchool in magic_schools_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_magic_schools(self)->list[MagicSchools]:
        try:
            items = await self.fetch_magic_schools()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "magic-schools",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_magic_schools(self)->list[MagicSchools]:
        try:
            await self.populate_magic_schools()

            collection = self.db["magic-schools"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [MagicSchools.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")