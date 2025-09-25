# app.py - Monolithic application file

# --- IMPORTS ---
import time
import uuid
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from asynctinydb import TinyDB, Query

# --- CONFIGURATION (from Config.py) ---
MAX_STAT: int = 100
STAT_DECAY_RATE: int = 2
HAPPINESS_DECAY_RATE: int = 3
MOOD_THRESHOLD_HAPPY: int = 70
MOOD_THRESHOLD_SAD: int = 30
GAME_INTERVAL_SECONDS: int = 7
LOCAL_STORAGE_KEY: str = "critterCraftPetMVP_v3"
FEED_HUNGER_RESTORE: int = 20
PLAY_HAPPINESS_BOOST: int = 25
PLAY_ENERGY_COST: int = 10
PET_ARCHETYPES: Dict[str, Dict[str, Any]] = {
    "sprite_glow": {"display_name": "Glow Sprite", "base_mood": "Curious", "base_stats": {"strength": 50, "agility": 60}},
    "sprite_crystal": {"display_name": "Crystal Sprite", "base_mood": "Calm", "base_stats": {"strength": 40, "agility": 70}},
    "sprite_bio": {"display_name": "Bio-Lume", "base_mood": "Playful", "base_stats": {"strength": 55, "agility": 55}},
}
PET_AURA_COLORS: Dict[str, str] = {
    "aura-blue": "#00aaff",
    "aura-green": "#00cc88",
    "aura-pink": "#ff66aa",
    "aura-gold": "#ffcc00",
}
AI_PERSONALITY_TRAITS: Dict[str, Any] = {
    "playfulness": {"min": 0, "max": 100, "default": 50},
    "curiosity": {"min": 0, "max": 100, "default": 50},
}
MIGRATION_READINESS_THRESHOLDS: Dict[str, int] = {
    "min_happiness": 60,
    "min_hunger": 40,
    "min_energy": 30,
    "min_interactions": 10,
}

# --- DATABASE (from database.py) ---
db = TinyDB("crittercraft.json")

# --- CORE LOGIC (from pet_core.py) ---
@dataclass
class InteractionRecord:
    timestamp: int
    type: str
    details: Optional[str] = None

@dataclass
class Pet:
    # Core Attributes
    name: str
    species: str
    aura_color: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # Vitals
    hunger: int = 50
    happiness: int = 50
    energy: int = 50

    # Dynamic Attributes
    mood: str = "Neutral"
    personality_traits: Dict[str, int] = field(default_factory=lambda: {
        k: v["default"] for k, v in AI_PERSONALITY_TRAITS.items()
    })

    # Timestamps & History
    creation_timestamp: int = field(default_factory=time.time_ns)
    last_active_timestamp: int = field(default_factory=time.time_ns)
    interaction_history: List[InteractionRecord] = field(default_factory=list)

    def _cap_stat(self, stat_value: int) -> int:
        return max(0, min(stat_value, MAX_STAT))

    def _update_mood(self):
        if self.happiness >= MOOD_THRESHOLD_HAPPY:
            self.mood = "Happy"
        elif self.happiness <= MOOD_THRESHOLD_SAD:
            self.mood = "Sad"
        else:
            self.mood = "Neutral"

    def _add_interaction_record(self, type: str, details: str):
        self.interaction_history.append(
            InteractionRecord(timestamp=time.time_ns(), type=type, details=details)
        )
        if len(self.interaction_history) > 100:
            self.interaction_history = self.interaction_history[-100:]

    def feed(self):
        self.hunger = self._cap_stat(self.hunger + FEED_HUNGER_RESTORE)
        self.happiness = self._cap_stat(self.happiness + 5)
        self._update_mood()
        self._add_interaction_record("feed", f"Restored {FEED_HUNGER_RESTORE} hunger.")

    def play(self):
        if self.energy < PLAY_ENERGY_COST:
            return False, "Pet is too tired to play!"

        self.energy = self._cap_stat(self.energy - PLAY_ENERGY_COST)
        self.happiness = self._cap_stat(self.happiness + PLAY_HAPPINESS_BOOST)
        self._update_mood()
        self._add_interaction_record("play", f"Boosted {PLAY_HAPPINESS_BOOST} happiness.")
        return True, "Played with pet!"

    def tick(self):
        current_time_ns = time.time_ns()
        time_diff_ns = current_time_ns - self.last_active_timestamp
        intervals_passed = time_diff_ns // (GAME_INTERVAL_SECONDS * 1_000_000_000)

        if intervals_passed > 0:
            self.hunger = self._cap_stat(self.hunger - int(STAT_DECAY_RATE * intervals_passed))
            self.energy = self._cap_stat(self.energy - int(STAT_DECAY_RATE * intervals_passed))
            self.happiness = self._cap_stat(self.happiness - int(HAPPINESS_DECAY_RATE * intervals_passed))
            self._update_mood()
            self.last_active_timestamp = current_time_ns

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Pet":
        interaction_history_data = data.get("interaction_history", [])
        data["interaction_history"] = [InteractionRecord(**rec) for rec in interaction_history_data]
        return cls(**data)

# --- API (from main.py) ---
app = FastAPI()

# Pydantic models
class PetCreate(BaseModel):
    name: str
    species: str
    aura_color: str

class InteractionRecordResponse(BaseModel):
    timestamp: int
    type: str
    details: Optional[str] = None

class PetResponse(BaseModel):
    id: str
    name: str
    species: str
    aura_color: str
    hunger: int
    happiness: int
    energy: int
    mood: str
    personality_traits: Dict[str, Any]
    creation_timestamp: int
    last_active_timestamp: int
    interaction_history: List[InteractionRecordResponse]

@app.post("/pets", response_model=PetResponse)
async def create_pet(pet_data: PetCreate):
    if pet_data.species not in PET_ARCHETYPES:
        raise HTTPException(status_code=400, detail="Invalid pet species")
    if pet_data.aura_color not in PET_AURA_COLORS:
        raise HTTPException(status_code=400, detail="Invalid aura color")

    new_pet = Pet(
        name=pet_data.name,
        species=pet_data.species,
        aura_color=pet_data.aura_color
    )

    await db.insert(new_pet.to_dict())
    return new_pet

@app.get("/pets/{pet_id}", response_model=PetResponse)
async def get_pet(pet_id: str):
    PetQuery = Query()
    pet_data = await db.search(PetQuery.id == pet_id)
    if not pet_data:
        raise HTTPException(status_code=404, detail="Pet not found")

    pet = Pet.from_dict(pet_data[0])
    pet.tick()

    await db.update(pet.to_dict(), PetQuery.id == pet_id)

    return pet

@app.post("/pets/{pet_id}/feed", response_model=PetResponse)
async def feed_pet(pet_id: str):
    PetQuery = Query()
    pet_data = await db.search(PetQuery.id == pet_id)
    if not pet_data:
        raise HTTPException(status_code=404, detail="Pet not found")

    pet = Pet.from_dict(pet_data[0])
    pet.feed()

    await db.update(pet.to_dict(), PetQuery.id == pet_id)
    return pet

@app.post("/pets/{pet_id}/play", response_model=PetResponse)
async def play_with_pet(pet_id: str):
    PetQuery = Query()
    pet_data = await db.search(PetQuery.id == pet_id)
    if not pet_data:
        raise HTTPException(status_code=404, detail="Pet not found")

    pet = Pet.from_dict(pet_data[0])
    success, message = pet.play()
    if not success:
        raise HTTPException(status_code=400, detail=message)

    await db.update(pet.to_dict(), PetQuery.id == pet_id)
    return pet

@app.get("/pets", response_model=List[PetResponse])
async def get_all_pets():
    all_pets_data = await db.all()
    return [Pet.from_dict(p) for p in all_pets_data]