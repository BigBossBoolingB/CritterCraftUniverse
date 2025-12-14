# prometheus_protocol/core/pet_core.py (Conceptual Path)
import json
import time
import uuid
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from config import ( # Import constants from config
    MAX_STAT, STAT_DECAY_RATE, HAPPINESS_DECAY_RATE,
    FEED_HUNGER_RESTORE, PLAY_HAPPINESS_BOOST, PLAY_ENERGY_COST,
    MOOD_THRESHOLD_HAPPY, MOOD_THRESHOLD_SAD,
    PET_ARCHETYPES, PET_AURA_COLORS, AI_PERSONALITY_TRAITS, # For initial pet creation
    GAME_INTERVAL_SECONDS
)

from trihorn_core import TrihornEngine

@dataclass
class InteractionRecord:
    """Represents a single interaction event with the pet."""
    timestamp: int     # Unix nanoseconds
    type: str          # e.g., "feed", "play", "chat", "train"
    details: Optional[str] = None # Optional details, e.g., "fed_berry"

@dataclass
class Pet:
    """
    Represents a CritterCraft Genesis Pet.
    This is the core data model for our AI digital companion.
    """
    name: str
    species: str            # e.g., 'sprite_glow', 'sprite_crystal'
    aura_color: str         # e.g., 'aura-blue', 'aura-gold'
    id: str = field(default_factory=lambda: str(uuid.uuid4())) # Unique ID for potential blockchain migration
    
    # Core Vitals (0-MAX_STAT)
    hunger: int = 50
    happiness: int = 50
    energy: int = 50
    
    # Training & Progression
    level: int = 1
    experience: int = 0
    intelligence: int = 10

    # Dynamic Attributes
    mood: str = "Neutral"   # Derived: "Happy", "Neutral", "Sad"
    
    # Personality Traits (Conceptual, for AI influence)
    personality_traits: Dict[str, int] = field(default_factory=lambda: {
        k: v["default"] for k, v in AI_PERSONALITY_TRAITS.items() # Initialize from config
    })
    
    creation_timestamp: int = field(default_factory=lambda: time.time_ns()) # Unix nanoseconds
    last_active_timestamp: int = field(default_factory=lambda: time.time_ns()) # For offline progress calculation
    
    interaction_history: List[InteractionRecord] = field(default_factory=list)

    # Initialize Trihorn engine (not serialized)
    _trihorn_engine: Optional[TrihornEngine] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Perform post-initialization validation and initial setup."""
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("Pet name cannot be empty.")
        if len(self.name) > 20: # Example limit
            raise ValueError("Pet name exceeds 20 characters.")
        
        if self.species not in PET_ARCHETYPES:
            raise ValueError(f"Invalid pet species: {self.species}")
        if self.aura_color not in PET_AURA_COLORS:
            raise ValueError(f"Invalid aura color: {self.aura_color}")

        self._trihorn_engine = TrihornEngine()
        self._update_mood() # Set initial mood based on happiness

    def _update_mood(self):
        """Update the pet's mood based on its happiness level."""
        if self.happiness >= MOOD_THRESHOLD_HAPPY:
            self.mood = "Happy"
        elif self.happiness <= MOOD_THRESHOLD_SAD:
            self.mood = "Sad"
        else:
            self.mood = "Neutral"

        # Trihorn Enhancement: Check for personality updates based on mood/state
        if self._trihorn_engine:
             # Just a simple conceptual hook
             pass

    def _add_interaction_record(self, type: str, details: Optional[str] = None):
        """Add a new interaction to the pet's history."""
        self.interaction_history.append(
            InteractionRecord(timestamp=time.time_ns(), type=type, details=details)
        )
        # Limit history size to prevent bloat (e.g., last 100 interactions)
        if len(self.interaction_history) > 100:
            self.interaction_history = self.interaction_history[-100:]

    def _cap_stat(self, stat_value: int) -> int:
        """Helper to cap stat values between 0 and MAX_STAT."""
        return max(0, min(stat_value, MAX_STAT))

    def feed(self):
        """Feed the pet, restoring hunger."""
        self.hunger = self._cap_stat(self.hunger + FEED_HUNGER_RESTORE)
        self.happiness = self._cap_stat(self.happiness + 5) # Small happiness boost
        self._update_mood()
        self._add_interaction_record("feed", f"Restored {FEED_HUNGER_RESTORE} hunger.")

        # Trihorn Enhancement: Consult engine for reaction
        narrative = "The pet eats happily."
        if self._trihorn_engine:
            analysis = self._trihorn_engine.process_query("User feeds the pet", self.__dict__)
            narrative = f"{analysis['Triadic Synthesis']}\n(Mysterium: {analysis['Mysterium Perspective']})"

        print(f"\n{narrative}")

    def play(self):
        """Play with the pet, boosting happiness and costing energy."""
        if self.energy < PLAY_ENERGY_COST:
            # Conceptual: AI could generate a pet refusal response ("too tired").
            return False, "Pet is too tired to play!"
        
        self.energy = self._cap_stat(self.energy - PLAY_ENERGY_COST)
        self.happiness = self._cap_stat(self.happiness + PLAY_HAPPINESS_BOOST)
        self._update_mood()
        self._add_interaction_record("play", f"Boosted {PLAY_HAPPINESS_BOOST} happiness.")

        # Trihorn Enhancement: Consult engine for reaction
        narrative = "The pet plays happily."
        if self._trihorn_engine:
            analysis = self._trihorn_engine.process_query("User plays with the pet", self.__dict__)
            narrative = f"{analysis['Triadic Synthesis']}\n(Logos: {analysis['Logos Perspective']})"

        return True, f"Played with pet!\n{narrative}"

    def train(self, training_type: str):
        """Train the pet with Trihorn supervision."""
        cost = PLAY_ENERGY_COST * 2
        if self.energy < cost:
             return False, "Pet is too mentally exhausted to train."

        self.energy = self._cap_stat(self.energy - cost)

        # Consult Trihorn
        if self._trihorn_engine:
             pet_state = self.__dict__.copy()
             pet_state.pop('_trihorn_engine', None)
             training_result = self._trihorn_engine.evaluate_training_session(pet_state, training_type)

             xp_gain = training_result.get("xp_gain", 10)
             self.experience += xp_gain

             # Level up logic
             if self.experience >= self.level * 100:
                 self.experience -= self.level * 100 # Preserve overflow XP
                 self.level += 1
                 self.intelligence += 5
                 level_up_msg = f"\nLEVEL UP! {self.name} is now level {self.level}!"
             else:
                 level_up_msg = ""

             self._add_interaction_record("train", f"{training_type} session. +{xp_gain} XP")

             return True, f"{training_result['narrative']}\nGained {xp_gain} XP.{level_up_msg}"
        else:
             return False, "Trihorn engine not active."

    def tick(self, current_time_ns: int):
        """
        Simulates the passage of time, decaying stats.
        Calculates offline progress if pet was inactive.
        """
        # Calculate time difference for offline progress
        time_diff_ns = current_time_ns - self.last_active_timestamp
        # Convert to game intervals
        intervals_passed = time_diff_ns // (GAME_INTERVAL_SECONDS * 1_000_000_000) # ns to seconds

        if intervals_passed > 0:
            self.hunger = self._cap_stat(self.hunger + int(STAT_DECAY_RATE * intervals_passed))
            self.energy = self._cap_stat(self.energy - int(STAT_DECAY_RATE * intervals_passed))
            self.happiness = self._cap_stat(self.happiness - int(HAPPINESS_DECAY_RATE * intervals_passed))
            self._update_mood()
            self.last_active_timestamp = current_time_ns # Update last active time

            # Conceptual: AI could analyze long periods of inactivity
            # and adjust personality traits (e.g., a "sad" trait might increase).
            # AI could also generate a pet comment about being lonely.
            # print(f"DEBUG: {intervals_passed} intervals passed. Stats decayed.") # For debug
        
        # Ensure stats don't go below 0 or above MAX_STAT (handled by _cap_stat, but double check)
        self.hunger = self._cap_stat(self.hunger)
        self.energy = self._cap_stat(self.energy)
        self.happiness = self._cap_stat(self.happiness)

    def status(self) -> str:
        """Return a string summary of the pet's current status."""
        return (
            f"{self.name} ({self.species}, {self.aura_color} aura)\n"
            f"Level: {self.level} (XP: {self.experience}/{self.level * 100})\n"
            f"Intelligence: {self.intelligence}\n"
            f"Mood: {self.mood}\n"
            f"Sustenance: {self.hunger}/{MAX_STAT}\n"
            f"Energy: {self.energy}/{MAX_STAT}\n"
            f"Happiness: {self.happiness}/{MAX_STAT}\n"
            f"Personality: {self.personality_traits}\n"
            f"Last Active: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(self.last_active_timestamp // 1_000_000_000))}"
            # Conceptual: AI could generate a more descriptive status based on pet's personality
        )

    def to_json(self) -> str:
        """Serialize the Pet object to a JSON string for persistence."""
        from dataclasses import asdict
        # Explicitly convert nested dataclasses (InteractionRecord) to dicts
        # We use asdict for the full tree conversion, then handle non-serializable fields if needed (though asdict handles basics well)
        # Note: asdict copies the object, so we don't modify self.

        # However, _trihorn_engine is not a field we want to serialize (and it's marked init=False, repr=False but asdict might include it if it was a field?)
        # _trihorn_engine is defined as field(init=False), so it is excluded from asdict by default? No, asdict includes all fields.
        # But we set it manually in __post_init__.
        # Let's use a simpler approach: serialize self.__dict__ but manually convert the history list to dicts.

        data = self.__dict__.copy()

        # Remove non-serializable runtime components
        if '_trihorn_engine' in data:
            del data['_trihorn_engine']

        # Convert InteractionRecord objects to dicts
        data['interaction_history'] = [asdict(rec) for rec in self.interaction_history]

        return json.dumps(data, default=str)

    @classmethod
    def from_json(cls, json_string: str) -> 'Pet':
        """Deserialize a Pet object from a JSON string."""
        data = json.loads(json_string)
        # Handle UUID string conversion back to UUID object if __init__ expects it
        # For simple string IDs, direct assignment is fine.
        data['id'] = str(data['id']) # Ensure it's string for consistency
        data['creation_timestamp'] = int(data['creation_timestamp'])
        data['last_active_timestamp'] = int(data['last_active_timestamp'])
        
        # Reconstruct InteractionRecord objects
        history = []
        for rec in data.get('interaction_history', []):
            if isinstance(rec, dict):
                history.append(InteractionRecord(**rec))
            else:
                # Fallback if it somehow got deserialized as an object already (unlikely with json.loads)
                # or if it's junk data
                pass
        data['interaction_history'] = history
        
        # Ensure personality_traits is a dict even if missing (from old data)
        data['personality_traits'] = data.get('personality_traits', {})
        
        # Dynamically set species and aura_color if they weren't in config (from old data)
        if 'species' not in data: data['species'] = PET_ARCHETYPES.keys().__iter__().__next__()
        if 'aura_color' not in data: data['aura_color'] = PET_AURA_COLORS.keys().__iter__().__next__()

        # Handle new fields for old saves
        if 'level' not in data: data['level'] = 1
        if 'experience' not in data: data['experience'] = 0
        if 'intelligence' not in data: data['intelligence'] = 10


        return cls(**data)
