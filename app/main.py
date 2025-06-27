from fastapi import FastAPI
from app.routes import spells, classes, abilityPoints,alignments, backgrounds, conditions, damageTypes, equipment,equipmentTypes

app = FastAPI(title="D&D 5e API Wrapper")

app.include_router(spells.router, prefix="/spells", tags=["spells"])

app.include_router(classes.router, prefix="/classes", tags=["classes"])

app.include_router(abilityPoints.router, prefix="/abilityPoints", tags=["abilityPoints"])

app.include_router(alignments.router, prefix="/alignments", tags=["alignments"])

app.include_router(backgrounds.router, prefix="/backgrounds", tags=["backgrounds"])

app.include_router(conditions.router, prefix="/conditions", tags=["conditions"])

app.include_router(damageTypes.router, prefix="/damageTypes", tags=["damageTypes"])

app.include_router(equipment.router, prefix="/equipment", tags=["equipment"])

app.include_router(equipmentTypes.router, prefix="/equipmentTypes", tags=["equipmentTypes"])

@app.get("/")
async def root():
    return {"message": "Bem vindo à Api D&D com FastAPI!"}


