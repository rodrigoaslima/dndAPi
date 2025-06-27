from app.db.repository import MongoRepository
import httpx
from fastapi import HTTPException
from app.config import BASE_URL
from app.models.alignments import Alignment

class AlignmentsService:
    def __init__(self,db):
        self.db = db
        self.repo = MongoRepository(db)
        self.base_url = BASE_URL

    async def fetch_alignment(self)->list[Alignment]:
       try:
           async with httpx.AsyncClient() as client:
               response = await client.get(f"{self.base_url}/alignments")
               response.raise_for_status()
               data = response.json()
               if not data:
                   raise HTTPException(status_code=500, detail="No alignment found")

               alignments_data = data.get("results", [])
               return [Alignment.from_dict(alignment) for alignment in alignments_data]

       except Exception as e:
           raise HTTPException(status_code=502, detail=f"Error in accessing external API: {str(e)}")

    async def populate_alignments(self)->list[Alignment]:
        try:
            items = await self.fetch_alignment()

            await self.repo.save_items_if_not_exist(
                items=items,
                collection_name="alignments",
                unique_field="index"
            )
            return items
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Error in saving items: {str(e)}")

    async def get_alignments(self)->list[Alignment]:
        try:
            await self.fetch_alignment()

            collection = self.db["alignments"]
            cursor = collection.find({})
            results = [doc async for doc in cursor]

            return [Alignment.from_dict(doc) for doc in results]
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Error in getting alignments: {str(e)}")