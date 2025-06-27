from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.classes import Classes

class ClassesService:
    def __init__(self, db):
        self.db = db
        self.repo = MongoRepository(db)
        self.base_url = BASE_URL

    async def fetch_classes(self)->list[Classes]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{BASE_URL}/classes/")
                response.raise_for_status()
                data = response.json()

                if not data:
                    raise HTTPException(status_code=500, detail="No classes found")

                classes_data = data.get("results", [])

                return [Classes.from_dict(classes) for classes in classes_data]

        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")


    async def populate_classes(self) -> list[Classes]:
        try:
            items = await self.fetch_classes()

            await self.repo.save_items_if_not_exist(
                items=items,
                collection_name="classes",
                unique_field="index"
            )
            return items
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_classes(self)->list[Classes]:
        try:
            await self.populate_classes()

            collection = self.db["classes"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]
            return [Classes.from_dict(doc) for doc in results]

        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Error in getting alignments: {str(e)}")