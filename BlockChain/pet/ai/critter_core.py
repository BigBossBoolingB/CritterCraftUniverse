# pet/critter_core.py
"""
Core functionality for the Critter-Craft application.

This module defines the Critter class, which represents a user-created
animal-inspired creature, and the ZoologistJournal class, which tracks
the user's progress and discoveries.

Following KISS principles:
- K (Know Your Core, Keep it Clear): Clear separation of data models and logic
- I (Iterate Intelligently): Structured for easy updates and maintenance
- S (Systematize for Scalability): Modular design with clear interfaces
- S (Sense the Landscape & Stimulate Engagement): Designed for user engagement
"""

from __future__ import annotations
import json
import time
import uuid
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field, asdict
from enum import Enum

# Import constants from the centralized config file
from .config import CritterCraftConfig

# --- Enums for Type Safety and Readability ---
class MaterialType(Enum):
    """Types of materials that can be used to craft a critter."""
    FUR = "fur"
    SCALES = "scales"
    FEATHERS = "feathers"
    SHELL = "shell"
    EXOSKELETON = "exoskeleton"
    
    @classmethod
    def from_string(cls, s: str) -> 'MaterialType':
        """Convert a string to a MaterialType enum member."""
        return cls(s.lower())

class AdaptationType(Enum):
    """Types of adaptations that can be applied to a critter."""
    CAMOUFLAGE = "camouflage"
    BIOLUMINESCENCE = "bioluminescence"
    ECHOLOCATION = "echolocation"
    MIMICRY = "mimicry"
    HIBERNATION = "hibernation"
    MIGRATION = "migration"
    SPECIALIZED_LIMBS = "specialized_limbs"
    
    @classmethod
    def from_string(cls, s: str) -> 'AdaptationType':
        """Convert a string to an AdaptationType enum member."""
        return cls(s.lower())

class BodyPosition(Enum):
    """Positions on a critter's body where materials or adaptations can be applied."""
    BODY = "body"
    HEAD = "head"
    LIMBS = "limbs"
    TAIL = "tail"
    WINGS = "wings"
    
    @classmethod
    def from_string(cls, s: str) -> 'BodyPosition':
        """Convert a string to a BodyPosition enum member."""
        return cls(s.lower())

class Environment(Enum):
    """Environments where a critter can be simulated."""
    FOREST = "forest"
    OCEAN = "ocean"
    DESERT = "desert"
    ARCTIC = "arctic"
    GRASSLAND = "grassland"
    
    @classmethod
    def from_string(cls, s: str) -> 'Environment':
        """Convert a string to an Environment enum member."""
        return cls(s.lower())

# --- Core Data Models ---
@dataclass
class CraftingMaterial:
    """Represents a material used in crafting a critter."""
    type: MaterialType
    color: str
    coverage: float  # 0.0 to 1.0
    position: BodyPosition

@dataclass
class Adaptation:
    """Represents an adaptation applied to a critter."""
    type: AdaptationType
    strength: int  # 1-10
    position: BodyPosition

@dataclass
class Critter:
    """
    Represents a user-created, animal-inspired creature.
    
    Following KISS principles:
    - K: Clear separation of data and validation
    - I: Structured for easy updates
    - S: Systematized with type-safe enums
    - S: Designed for user engagement
    """
    name: str
    base_animal: str  # e.g., "chameleon", "anglerfish"
    creator_name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    materials: List[CraftingMaterial] = field(default_factory=list)
    adaptations: List[Adaptation] = field(default_factory=list)
    facts_learned: Set[str] = field(default_factory=set)
    
    creation_timestamp: int = field(default_factory=time.time_ns)
    last_modified_timestamp: int = field(default_factory=time.time_ns)
    
    zoologist_level: str = 'novice'

    def __post_init__(self):
        """Perform post-initialization validation."""
        self.name = self.name.strip()
        if not self.name or len(self.name) > 20:
            raise ValueError("Critter name must be 1-20 characters.")
        
        if self.base_animal not in CritterCraftConfig.CRITTER_TYPES:
            raise ValueError(f"Invalid base animal: {self.base_animal}")

    def add_material(self, material_type: str, color: str, coverage: float, position: str):
        """Add a crafting material to the critter."""
        material = CraftingMaterial(
            type=MaterialType.from_string(material_type),
            color=color,
            coverage=coverage,
            position=BodyPosition.from_string(position)
        )
        self.materials.append(material)
        self.last_modified_timestamp = time.time_ns()

    def add_adaptation(self, adaptation_type: str, strength: int, position: str):
        """Add an adaptation to the critter."""
        adaptation = Adaptation(
            type=AdaptationType.from_string(adaptation_type),
            strength=strength,
            position=BodyPosition.from_string(position)
        )
        self.adaptations.append(adaptation)
        self.last_modified_timestamp = time.time_ns()

    def learn_fact(self, fact: str):
        """Record that the user has learned a fact about the base animal."""
        self.facts_learned.add(fact)
        self.last_modified_timestamp = time.time_ns()

    def get_info_card(self) -> str:
        """Get a formatted string with the critter's information."""
        base_animal_info = CritterCraftConfig.CRITTER_TYPES.get(self.base_animal, {})
        base_animal_display = base_animal_info.get('display_name', self.base_animal)

        info = [
            f"--- {self.name} ---",
            f"Base Animal: {base_animal_display}",
            f"Creator: {self.creator_name}",
            f"Zoologist Level: {self.zoologist_level.capitalize()}",
            "\n--- Materials ---"
        ]
        
        if self.materials:
            for material in self.materials:
                info.append(f"- {material.color} {material.type.value} on {material.position.value} ({material.coverage:.0%})")
        else:
            info.append("No materials added yet.")

        info.append("\n--- Adaptations ---")
        if self.adaptations:
            for adaptation in self.adaptations:
                adaptation_info = CritterCraftConfig.ADAPTATIONS.get(adaptation.type.value, {})
                adaptation_display = adaptation_info.get('display_name', adaptation.type.value)
                info.append(f"- {adaptation_display} (Strength: {adaptation.strength}) on {adaptation.position.value}")
        else:
            info.append("No adaptations added yet.")
        
        info.append("\n--- Learned Facts ---")
        if self.facts_learned:
            for fact in self.facts_learned:
                info.append(f"- {fact}")
        else:
            info.append("No facts learned yet.")
        
        return "\n".join(info)

    def simulate_in_environment(self, environment: str) -> Dict[str, Any]:
        """Simulate how the critter performs in a given environment."""
        env = Environment.from_string(environment)
        results = {
            'environment': env.value,
            'survival_score': 50,
            'advantages': [],
            'disadvantages': []
        }
        
        # Base animal habitat
        base_animal_info = CritterCraftConfig.CRITTER_TYPES.get(self.base_animal, {})
        natural_habitat = base_animal_info.get('habitat', '').lower()
        
        if env.value in natural_habitat:
            results['survival_score'] += 20
            results['advantages'].append("Well-suited to its natural habitat.")
        else:
            results['survival_score'] -= 10
            results['disadvantages'].append("Not in its natural habitat.")

        # Adaptations
        for adaptation in self.adaptations:
            # Simple simulation logic - can be expanded
            if adaptation.type == AdaptationType.CAMOUFLAGE and env in [Environment.FOREST, Environment.GRASSLAND]:
                results['survival_score'] += adaptation.strength
                results['advantages'].append("Camouflage provides excellent cover.")
            elif adaptation.type == AdaptationType.BIOLUMINESCENCE and env == Environment.OCEAN:
                results['survival_score'] += adaptation.strength
                results['advantages'].append("Bioluminescence is effective in the deep ocean.")
            else:
                results['survival_score'] -= 2 # Minor penalty for non-optimal adaptations
        
        return results

@dataclass
class ZoologistJournal:
    """
    Tracks a user's progress, discoveries, and created critters.
    """
    username: str
    critters_created: int = 0
    facts_learned: Set[str] = field(default_factory=set)
    unlocked_materials: Set[MaterialType] = field(default_factory=lambda: {MaterialType.FUR, MaterialType.SCALES})
    unlocked_adaptations: Set[AdaptationType] = field(default_factory=lambda: {AdaptationType.CAMOUFLAGE, AdaptationType.SPECIALIZED_LIMBS})

    def add_critter(self):
        """Increment the count of created critters."""
        self.critters_created += 1
        self._check_for_level_up()

    def learn_fact(self, fact: str):
        """Add a new fact to the journal."""
        if fact not in self.facts_learned:
            self.facts_learned.add(fact)

    def _check_for_level_up(self):
        """Check if the user has met the requirements for the next level."""
        current_level = self.get_level()
        level_order = list(CritterCraftConfig.ZOOLOGIST_LEVELS.keys())
        current_index = level_order.index(current_level)

        if current_index < len(level_order) - 1:
            next_level = level_order[current_index + 1]
            requirements = CritterCraftConfig.ZOOLOGIST_LEVELS[next_level]

            if self.critters_created >= requirements['required_critters']:
                # Unlock new items
                new_materials = requirements.get('unlocked_materials', [])
                for material in new_materials:
                    self.unlocked_materials.add(MaterialType.from_string(material))

                new_adaptations = requirements.get('unlocked_adaptations', [])
                for adaptation in new_adaptations:
                    self.unlocked_adaptations.add(AdaptationType.from_string(adaptation))

    def get_level(self) -> str:
        """Get the current zoologist level."""
        level_order = list(CritterCraftConfig.ZOOLOGIST_LEVELS.keys())
        for i in range(len(level_order) - 1, -1, -1):
            level = level_order[i]
            if self.critters_created >= CritterCraftConfig.ZOOLOGIST_LEVELS[level]['required_critters']:
                return level
        return 'novice'

# --- Persistence Functions ---
class CritterPersistence:
    """Handles saving and loading critters to/from storage."""
    
    @staticmethod
    def save_to_file(critter: Critter, filename: str) -> bool:
        """Saves a critter's state to a JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump(asdict(critter), f, indent=4)
            return True
        except (IOError, TypeError) as e:
            print(f"Error saving critter to {filename}: {e}")
            return False

    @staticmethod
    def load_from_file(filename: str) -> Optional[Critter]:
        """Loads a critter's state from a JSON file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            return Critter(**data)
        except (IOError, json.JSONDecodeError, KeyError) as e:
            print(f"Error loading critter from {filename}: {e}")
            return None
