import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from crittercraft.pet_core import Pet
from crittercraft.vdatabprot import save, load

class TestStorageIntegration(unittest.TestCase):
    def test_save_load_roundtrip(self):
        """
        Tests that a pet object can be saved and then loaded,
        and that the loaded object is identical to the original.
        """
        # 1. Instantiate
        original_pet = Pet(name="TestPet", species="sprite_glow", aura_color="aura-blue")

        # 2. Save
        save(original_pet.id, original_pet.to_json())

        # 3. Load
        loaded_pet_json = load(original_pet.id)
        self.assertIsNotNone(loaded_pet_json)
        loaded_pet = Pet.from_json(loaded_pet_json)

        # 4. Assert
        self.assertEqual(original_pet.id, loaded_pet.id)
        self.assertEqual(original_pet.name, loaded_pet.name)
        self.assertEqual(original_pet.species, loaded_pet.species)
        self.assertEqual(original_pet.aura_color, loaded_pet.aura_color)
        self.assertEqual(original_pet.hunger, loaded_pet.hunger)
        self.assertEqual(original_pet.happiness, loaded_pet.happiness)
        self.assertEqual(original_pet.energy, loaded_pet.energy)

if __name__ == "__main__":
    unittest.main()
