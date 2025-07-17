from fastapi import FastAPI
from app.routes import (spells, classes, abilityPoints,alignments, backgrounds, conditions,
                        damageTypes, equipment,equipmentTypes,feats, features, languages,
                        magicItems, magicSchools, monsters, proficiencies, races, ruleSections,
                        rules, skills, subclasses, subraces, traits, weaponProperties,characters)

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

app.include_router(feats.router, prefix="/feats", tags=["feats"])

app.include_router(features.router, prefix="/features", tags=["features"])

app.include_router(languages.router, prefix="/languages", tags=["languages"])

app.include_router(magicItems.router, prefix="/magicItems", tags=["magicItems"])

app.include_router(magicSchools.router, prefix="/magicSchools", tags=["magicSchools"])

app.include_router(monsters.router, prefix="/monsters", tags=["monsters"])

app.include_router(proficiencies.router, prefix="/proficiencies", tags=["proficiencies"])

app.include_router(races.router, prefix="/races", tags=["races"])

app.include_router(ruleSections.router, prefix="/ruleSections", tags=["ruleSections"])

app.include_router(rules.router, prefix="/rules", tags=["rules"])

app.include_router(skills.router, prefix="/skills", tags=["skills"])

app.include_router(subclasses.router, prefix="/subclasses", tags=["subclasses"])

app.include_router(subraces.router, prefix="/subraces", tags=["subraces"])

app.include_router(traits.router, prefix="/traits", tags=["traits"])

app.include_router(weaponProperties.router, prefix="/weaponProperties", tags=["weaponProperties"])

app.include_router(characters.router, prefix="/characters", tags=["characters"])

@app.get("/")
async def root():
    return {"message": "Bem vindo à Api D&D com FastAPI!"}


