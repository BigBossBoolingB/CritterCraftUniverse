"""
Unified and Strategic Configuration for the CritterCraft Universe.

This module applies the Expanded KISS Principle to centralize all game parameters
for both the 'Genesis Pet' and 'Critter-Craft' systems. By using Enums and
namespaced classes, it provides a single, clear, robust, and easily tunable
source of truth for game designers and developers.

Principles Applied:
- K (Know Your Core, Keep it Clear): Concepts are separated into distinct classes.
  Enums create a clear, typo-proof vocabulary for core stats and traits.
- S (Systematize for Scalability): A single Stat enum is the source of truth,
  and all related dictionaries are systematically derived from it. The
  hierarchical class structure is scalable for future additions.
- I (Iterate Intelligently): Errors from the original files (duplicates,
  typos) have been fixed. The structure is easy to modify for game balancing.
"""

from enum import Enum, auto

# ==============================================================================
# --- CORE ENUM DEFINITIONS (Single Source of Truth) ---
# ==============================================================================

class Stat(Enum):
    """The single source of truth for all primary pet statistics."""
    HUNGER = "Sustenance"
    ENERGY = "Energy"
    HAPPINESS = "Happiness"
    IQ = "Intelligence"
    CHARISMA = "Charisma"
    CLEANLINESS = "Cleanliness"
    SOCIAL = "Social"

class PersonalityTrait(Enum):
    """Defines the core personality dimensions."""
    PLAYFULNESS = auto()
    CURIOSITY = auto()
    SOCIABILITY = auto()
    INDEPENDENCE = auto()
    LOYALTY = auto()
    ADVENTUROUSNESS = auto()
    INTELLIGENCE = auto()
    EMPATHY = auto()
    CALMNESS = auto()
    STUBBORNNESS = auto()

class Topic(Enum):
    GREETING = auto()
    WELL_BEING = auto()
    PLAY = auto()
    FOOD = auto()
    LEARNING = auto()
    COMPLIMENT = auto()
    ENVIRONMENT = auto()
    ADVENTURE = auto()
    FRIENDSHIP = auto()
    EMOTIONS = auto()

class Mood(Enum):
    ECSTATIC = auto()
    HAPPY = auto()
    NEUTRAL = auto()
    GRUMPY = auto()
    SAD = auto()
    MISERABLE = auto()
    ANXIOUS = auto()
    EXCITED = auto()
    BORED = auto()
    FRUSTRATED = auto()
    CONTENT = auto()

class MemoryType(Enum):
    INTERACTION = auto()
    PREFERENCE = auto()
    FACT = auto()
    MILESTONE = auto()
    EMOTION = auto()
    EXPERIENCE = auto()
    SKILL = auto()
    RELATIONSHIP = auto()

# ==============================================================================
# --- I. GENESIS PET CONFIGURATION ---
# ==============================================================================

class GenesisPetConfig:
    """A namespace for all settings related to the core virtual pet experience."""

    class Core:
        """Global mechanics and thresholds."""
        MAX_STAT = 100
        DECAY_INTERVAL_SECONDS = 3600
        INITIAL_STATS = {
            Stat.HUNGER: 50,
            Stat.ENERGY: 70,
            Stat.HAPPINESS: 60,
            Stat.IQ: 10,
            Stat.CHARISMA: 10,
            Stat.CLEANLINESS: 80,
            Stat.SOCIAL: 50,
        }
        DECAY_RATES = {
            Stat.HUNGER: 5,
            Stat.ENERGY: -3,
            Stat.HAPPINESS: -2,
            Stat.CLEANLINESS: -5,
            Stat.SOCIAL: -3,
            Stat.IQ: 0,
            Stat.CHARISMA: 0,
        }

    class Interactions:
        EFFECTS = {
            'feed': {
                'stat_changes': {Stat.HUNGER: -30, Stat.HAPPINESS: 5, Stat.CLEANLINESS: -10},
                'min_energy': 5,
                'messages': {
                    'success': "{pet_name} happily munches on the treat!",
                    'too_full': "{pet_name} seems too full to eat right now.",
                }
            },
            'play': {
                'stat_changes': {Stat.ENERGY: -20, Stat.HAPPINESS: 25, Stat.HUNGER: 10, Stat.SOCIAL: 15},
                'min_energy': 15,
                'messages': {
                    'success': "{pet_name} leaps with joy while playing with you!",
                    'too_tired': "{pet_name} is too tired to play. Let them rest.",
                }
            },
            'chat': {
                'stat_changes': {Stat.IQ: 3, Stat.HAPPINESS: 8, Stat.ENERGY: -5, Stat.SOCIAL: 10},
                'min_energy': 5,
                'messages': { 'success': "{pet_name} chirps thoughtfully." }
            },
            'groom': {
                'stat_changes': {Stat.CLEANLINESS: 40, Stat.HAPPINESS: 10, Stat.ENERGY: -5},
                'min_energy': 0,
                'messages': { 'success': "{pet_name} gleams after a good grooming session!" }
            }
        }

    class Moods:
        THRESHOLDS = [
            {'name': 'Ecstatic', 'threshold': 90, 'emoji': '🤩'},
            {'name': 'Happy', 'threshold': 75, 'emoji': '😊'},
            {'name': 'Neutral', 'threshold': 45, 'emoji': '😐'},
            {'name': 'Grumpy', 'threshold': 25, 'emoji': '😒'},
            {'name': 'Sad', 'threshold': 10, 'emoji': '😔'},
            {'name': 'Miserable', 'threshold': 0, 'emoji': '😭'},
        ]
        STATUS_ALERTS = {
            'hunger_critical': {'stat': Stat.HUNGER, 'condition': lambda v: v >= 80, 'message': "is very hungry!"},
            'energy_critical': {'stat': Stat.ENERGY, 'condition': lambda v: v <= 20, 'message': "is extremely tired!"},
            'cleanliness_low': {'stat': Stat.CLEANLINESS, 'condition': lambda v: v <= 30, 'message': "is looking a bit messy."},
            'social_low': {'stat': Stat.SOCIAL, 'condition': lambda v: v <= 20, 'message': "craves your attention!"},
        }

    class Archetypes:
        DEFINITIONS = {
            'sprite_glow': {
                'display_name': 'Glowing Sprite', 'rarity': 'Common',
                'stat_modifiers': {Stat.ENERGY: 10, Stat.IQ: 5}
            },
            'sprite_crystal': {
                'display_name': 'Crystal Sprite', 'rarity': 'Uncommon',
                'stat_modifiers': {Stat.HAPPINESS: 5, Stat.SOCIAL: -10}
            },
            'sprite_shadow': {
                'display_name': 'Shadow Sprite', 'rarity': 'Rare',
                'stat_modifiers': {Stat.SOCIAL: -20, Stat.CHARISMA: 10},
                'decay_modifiers': {Stat.SOCIAL: -0.2}
            },
            # ... Add other archetypes here ...
        }

    class Auras:
        DEFINITIONS = {
            'aura-blue': {
                'display_name': 'Sapphire Blue',
                'stat_boosts': {Stat.IQ: 0.05, Stat.HAPPINESS: 0.02}
            },
            'aura-gold': {
                'display_name': 'Radiant Gold',
                'stat_boosts': {Stat.CHARISMA: 0.10, Stat.SOCIAL: 0.05}
            },
            # ... Add other auras here ...
        }

    class Personality:
        TRAITS = {
            trait: {'min': 0, 'max': 100, 'default': 50} for trait in PersonalityTrait
        }

    class Progression:
        MIGRATION_READINESS = {
            'min_stats': {Stat.HAPPINESS: 75, Stat.ENERGY: 65, Stat.IQ: 20, Stat.CHARISMA: 15},
            'max_stats': {Stat.HUNGER: 25},
            'min_interactions': 30,
            'min_days_owned': 7
        }

# ==============================================================================
# --- II. CRITTER-CRAFT CONFIGURATION ---
# ==============================================================================

PET_ARCHETYPES = {
    'sprite_glow': {
        'display_name': 'Glowing Sprite',
        'description': 'A luminous, ethereal creature that radiates gentle light. Often curious and energetic.',
        'traits': ['curious', 'playful', 'energetic'],
        'rarity': 'Common',
        'base_stats_modifier': {'energy': 10, 'iq': 5}, # Start with more energy and intelligence
        'aura_effect_modifier': {'energy': 0.1, 'happiness': 0.05}, # Aura effects are 10% more potent for this species
        'aging_rate': 6  # Ages 6x faster than humans after first year
    },
    'sprite_crystal': {
        'display_name': 'Crystal Sprite',
        'description': 'A crystalline entity with a faceted body that refracts light beautifully. Calm and patient.',
        'traits': ['calm', 'wise', 'patient'],
        'rarity': 'Uncommon',
        'base_stats_modifier': {'happiness': 5, 'social': -10}, # Slightly happier, less social
        'trait_modifiers': {'playfulness': -0.1, 'curiosity': 0.05}, # 10% less playful, 5% more curious over time
        'aging_rate': 4  # Ages 4x faster than humans after first year
    },
    'sprite_shadow': {
        'display_name': 'Shadow Sprite',
        'description': 'A mysterious being composed of shifting shadows and dark energy. Independent and observant.',
        'traits': ['mysterious', 'independent', 'observant'],
        'rarity': 'Rare',
        'base_stats_modifier': {'social': -20, 'charisma': 10}, # Very independent, charming in a dark way
        'decay_rate_modifier': {'social': -0.2}, # Social stat decays 20% slower
        'interaction_boosts': {'chat': {'iq': 2}} # Chatting boosts IQ even more for Shadow Sprites
    },
    'sprite_ember': {
        'display_name': 'Ember Sprite',
        'description': 'A warm, fiery creature with a passionate spirit. Brave and protective.',
        'traits': ['passionate', 'brave', 'protective'],
        'rarity': 'Uncommon',
        'base_stats_modifier': {'energy': 20, 'happiness': -5}, # More energetic, slightly moodier
        'decay_rate_modifier': {'energy': -0.1} # Energy decays 10% slower
    },
    'sprite_aqua': {
        'display_name': 'Aqua Sprite',
        'description': 'A fluid, water-like being that flows with grace and adaptability. Peaceful and creative.',
        'traits': ['adaptable', 'peaceful', 'creative'],
        'rarity': 'Uncommon',
        'base_stats_modifier': {'cleanliness': 10, 'iq': 5}, # Naturally cleaner and smarter
        'interaction_boosts': {'groom': {'happiness': 5}} # Grooming provides extra happiness for Aqua Sprites
    }
}

PET_AURA_COLORS = {
    'aura-blue': {
        'display_name': 'Sapphire Blue',
        'description': 'A calming blue aura that soothes the mind.',
        'effect': 'Increases wisdom and patience.',
        'stat_boosts': {'iq': 0.05, 'happiness': 0.02}, # 5% IQ boost, 2% happiness boost
        'decay_reduction': {'energy': 0.03} # Reduces energy decay by 3%
    },
    'aura-gold': {
        'display_name': 'Radiant Gold',
        'description': 'A brilliant golden aura that inspires confidence.',
        'effect': 'Boosts charisma and leadership.',
        'stat_boosts': {'charisma': 0.10, 'social': 0.05},
    },
    'aura-green': {
        'display_name': 'Emerald Green',
        'description': 'A nurturing green aura connected to growth and healing.',
        'effect': 'Enhances growth and recovery rates.',
        'stat_boosts': {'energy': 0.03, 'cleanliness': 0.05},
        'decay_reduction': {'hunger': 0.02} # Reduces hunger decay by 2%
    },
    'aura-purple': {
        'display_name': 'Mystic Purple',
        'description': 'A mysterious purple aura linked to psychic abilities.',
        'effect': 'Improves intuition and perception.',
        'stat_boosts': {'iq': 0.08, 'social': -0.01}, # IQ boost, slight social reduction
    },
    'aura-red': {
        'display_name': 'Passionate Red',
        'description': 'An energetic red aura full of vitality.',
        'effect': 'Increases energy and determination.',
        'stat_boosts': {'energy': 0.12},
        'decay_reduction': {'happiness': 0.01} # Slightly reduces happiness decay
    }
}

AI_PERSONALITY_TRAITS = {
    'playfulness': {
        'description': 'Influences the pet\'s playful and energetic responses.',
        'default': 50,
        'min': 0,
        'max': 100
    },
    'curiosity': {
        'description': 'Determines how interested the pet is in exploring and learning.',
        'default': 50,
        'min': 0,
        'max': 100
    },
    'sociability': {
        'description': 'Governs the pet\'s enjoyment of interaction and social engagement.',
        'default': 50,
        'min': 0,
        'max': 100
    },
    'independence': {
        'description': 'Indicates how self-sufficient the pet is when left alone, affecting clinginess.',
        'default': 50,
        'min': 0,
        'max': 100
    },
    'loyalty': {
        'description': 'Reflects the pet\'s devotion to its owner.',
        'default': 50,
        'min': 0,
        'max': 100
    }
}

MIGRATION_READINESS_THRESHOLDS = {
    'min_happiness': 75,
    'min_energy': 65,
    'max_hunger': 25,
    'min_interactions': 30,
    'min_days_owned': 7,
    'min_iq': 20,
    'min_charisma': 15,
}

MOOD_THRESHOLD_HAPPY = 75
MOOD_THRESHOLD_SAD = 25

class CritterCraftConfig:
    """A namespace for all settings related to the animal-crafting game concept."""

    CRITTER_TYPES = {
        'chameleon': {
            'display_name': 'Chameleon', 'habitat': 'Tropical forests',
            'adaptations': ['camouflage', 'prehensile_tail', 'rotating_eyes']
        },
        'anglerfish': {
            'display_name': 'Anglerfish', 'habitat': 'Deep ocean',
            'adaptations': ['bioluminescence', 'large_jaw', 'sharp_teeth']
        },
        # ... Add other critter types here ...
    }

    ADAPTATIONS = {
        'camouflage': {
            'display_name': 'Camouflage',
            'description': 'The ability to blend in with surroundings.'
        },
        'bioluminescence': {
            'display_name': 'Bioluminescence',
            'description': 'The production of light by living organisms.'
        },
        # ... Add other adaptations here ...
    }

    ZOOLOGIST_LEVELS = {
        'novice': {'required_critters': 3, 'unlocks': "Basic Materials"},
        'apprentice': {'required_critters': 7, 'unlocks': "Feathers"},
        # ... Add other levels here ...
    }

# ==============================================================================
# --- AI/CONVERSATION CONFIGURATION ---
# ==============================================================================

CONVERSATION_TOPICS_CONFIG = {
    Topic.GREETING: {'keywords': ['hello', 'hi', 'hey'], 'importance': 3},
    Topic.WELL_BEING: {'keywords': ['how are you', 'feeling'], 'importance': 3},
    Topic.PLAY: {'keywords': ['play', 'game', 'fun'], 'importance': 2},
    Topic.FOOD: {'keywords': ['food', 'hungry', 'eat'], 'importance': 2},
    Topic.LEARNING: {'keywords': ['learn', 'teach', 'knowledge'], 'importance': 2},
    Topic.COMPLIMENT: {'keywords': ['good job', 'well done', 'great'], 'importance': 3},
    Topic.ENVIRONMENT: {'keywords': ['weather', 'outside', 'nature'], 'importance': 2},
    Topic.ADVENTURE: {'keywords': ['explore', 'adventure', 'journey'], 'importance': 1},
    Topic.FRIENDSHIP: {'keywords': ['friend', 'buddy', 'pal'], 'importance': 3},
    Topic.EMOTIONS: {'keywords': ['happy', 'sad', 'angry'], 'importance': 3},
    # Add other topics as needed...
}

MOOD_RESPONSE_MODIFIERS = {
    Mood.ECSTATIC: "Your pet is thrilled and ready for anything!",
    Mood.HAPPY: "Your pet seems cheerful and playful.",
    Mood.NEUTRAL: "Your pet is calm and relaxed.",
    Mood.GRUMPY: "Your pet is not in the best mood; approach with care.",
    Mood.SAD: "Your pet seems a bit down; maybe some playtime will help.",
    Mood.MISERABLE: "Your pet is feeling very low; comfort it gently.",
    Mood.ANXIOUS: "Your pet appears uneasy; try to reassure it.",
    Mood.EXCITED: "Your pet is buzzing with energy!",
    Mood.BORED: "Your pet looks like it needs something fun to do.",
    Mood.FRUSTRATED: "Your pet is feeling annoyed; give it some space.",
    Mood.CONTENT: "Your pet is satisfied and enjoying the moment.",
}

PERSONALITY_RESPONSE_MODIFIERS = {
    PersonalityTrait.PLAYFULNESS: "Your pet loves to play and will enjoy games.",
    PersonalityTrait.CURIOSITY: "Your pet is eager to explore new things.",
    PersonalityTrait.SOCIABILITY: "Your pet enjoys being around others.",
    PersonalityTrait.INDEPENDENCE: "Your pet likes to do things on its own.",
    PersonalityTrait.LOYALTY: "Your pet is very loyal and protective.",
    PersonalityTrait.ADVENTUROUSNESS: "Your pet is always up for an adventure!",
    PersonalityTrait.INTELLIGENCE: "Your pet can solve problems quickly.",
    PersonalityTrait.EMPATHY: "Your pet understands your feelings well.",
    PersonalityTrait.CALMNESS: "Your pet remains composed in stressful situations.",
    PersonalityTrait.STUBBORNNESS: "Your pet can be quite headstrong at times.",
}

SPECIES_SPEECH_PATTERNS = {
    "dog": {
        "bark": "Woof!",
        "whine": "Whimper...",
        "growl": "Grrr...",
    },
    "cat": {
        "meow": "Meow!",
        "purr": "Purr...",
        "hiss": "Hiss!",
    },
    # Add other species as needed...
}

AURA_INFLUENCE = {
    "positive": "Your pet's positive aura boosts the mood of those around it.",
    "neutral": "Your pet's neutral aura has a calming effect.",
    "negative": "Your pet's negative aura may cause discomfort to others.",
}

MEMORY_TYPES_CONFIG = {
    MemoryType.INTERACTION: {
        "description": "Memories of interactions with others.",
        "examples": ["First meeting", "Playtime", "Feeding"],
    },
    MemoryType.PREFERENCE: {
        "description": "Preferences for activities or items.",
        "examples": ["Favorite toy", "Preferred food", "Favorite game"],
    },
    MemoryType.FACT: {
        "description": "General facts learned over time.",
        "examples": ["Knows its name", "Recognizes commands"],
    },
    MemoryType.MILESTONE: {
        "description": "Significant events in the pet's life.",
        "examples": ["First birthday", "First adventure"],
    },
    MemoryType.EMOTION: {
        "description": "Memories of emotional states.",
        "examples": ["Happy after playtime", "Sad when left alone"],
    },
    MemoryType.EXPERIENCE: {
        "description": "Memories of significant experiences.",
        "examples": ["First trip to the park", "Meeting new friends"],
    },
    MemoryType.SKILL: {
        "description": "Skills learned by the pet.",
        "examples": ["Sit", "Stay", "Roll over"],
    },
    MemoryType.RELATIONSHIP: {
        "description": "Memories of relationships with other pets or humans.",
        "examples": ["Best friend", "Favorite human"],
    },
}

# ==============================================================================
# --- CONFIGURATION VALIDATION ---
# ==============================================================================
def _validate_config():
    """(I) Internal function to validate configuration consistency on import."""
    all_stats = set(Stat)

    # Validate that all stat keys in the config are valid Stat Enum members
    for data in GenesisPetConfig.Archetypes.DEFINITIONS.values():
        for stat_key in data.get('stat_modifiers', {}):
            if stat_key not in all_stats:
                raise ValueError(f"Invalid stat '{stat_key}' in Archetypes.")

    for data in GenesisPetConfig.Interactions.EFFECTS.values():
        for stat_key in data.get('stat_changes', {}):
            if stat_key not in all_stats:
                raise ValueError(f"Invalid stat '{stat_key}' in Interactions.")
    
    # Ensure every stat has a decay rate defined
    if set(GenesisPetConfig.Core.DECAY_RATES.keys()) != all_stats:
        raise ValueError("DECAY_RATES must define a rate for every member of the Stat enum.")

# Run validation automatically when the module is imported
_validate_config()
