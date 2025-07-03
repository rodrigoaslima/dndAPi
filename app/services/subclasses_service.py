from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.subclasses import Subclasses

class SubclassesService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(self.db)
        self.base_url = BASE_URL

    async def fetch_subclasses(self)-> list[Subclasses]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/subclasses")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No subclasses found")

                subclasses_data = data.get("results", [])

                return [Subclasses.from_dict(subclass) for subclass in subclasses_data]
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_subclasses(self)->list[Subclasses]:
        try:
            items = await self.fetch_subclasses()

            await self.repo.save_items_if_not_exist(
                items = items,
                collection_name = "subclasses",
                unique_field="index"
            )
            return items
        except HTTPException as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_subclasses(self)->list[Subclasses]:
        try:
            await self.populate_subclasses()

            collection = self.db["subclasses"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [Subclasses.from_dict(doc) for doc in results]
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error reading from DB: {str(e)}")