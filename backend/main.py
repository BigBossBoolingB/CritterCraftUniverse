from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

from .pet_core import Pet
from .Config import PET_ARCHETYPES, PET_AURA_COLORS

app = FastAPI()

# In-memory database for storing pets
pets_db: Dict[str, Pet] = {}

class PetCreate(BaseModel):
    name: str
    species: str
    aura_color: str

@app.post("/pets", response_model=Pet)
def create_pet(pet_data: PetCreate):
    if pet_data.species not in PET_ARCHETYPES:
        raise HTTPException(status_code=400, detail="Invalid pet species")
    if pet_data.aura_color not in PET_AURA_COLORS:
        raise HTTPException(status_code=400, detail="Invalid aura color")

    new_pet = Pet(
        name=pet_data.name,
        species=pet_data.species,
        aura_color=pet_data.aura_color
    )
    pets_db[new_pet.id] = new_pet
    return new_pet

@app.get("/pets/{pet_id}", response_model=Pet)
def get_pet(pet_id: str):
    pet = pets_db.get(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

@app.post("/pets/{pet_id}/feed", response_model=Pet)
def feed_pet(pet_id: str):
    pet = pets_db.get(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    pet.feed()
    return pet

@app.post("/pets/{pet_id}/play", response_model=Pet)
def play_with_pet(pet_id: str):
    pet = pets_db.get(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    success, message = pet.play()
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return pet