import unittest
import json
from main import app, save_pet
from pet.ai.pet_core import Pet, PetLogicManager
from pet.ai.config import PET_ARCHETYPES, PET_AURA_COLORS

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.pet = Pet(name="Test Pet", species="sprite_glow", aura_color="aura-blue")
        self.pet_manager = PetLogicManager(self.pet)
        save_pet(self.pet)

    def test_get_pet_status(self):
        response = self.app.get(f'/api/pet/status/{self.pet.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test Pet')

    def test_interact_with_pet(self):
        response = self.app.post('/api/pet/interact',
                                     data=json.dumps({'pet_id': self.pet.id, 'interaction_type': 'feed'}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

    def test_get_user_wallet(self):
        response = self.app.get('/api/user/wallet/456')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('qrasl_balance', data)

if __name__ == '__main__':
    unittest.main()
