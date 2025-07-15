const API_BASE_URL = 'http://localhost:5000/api';

const critterCraftAPI = {
  getPetStatus: async (petId) => {
    const response = await fetch(`${API_BASE_URL}/pet/status/${petId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch pet status');
    }
    return response.json();
  },

  interactWithPet: async (petId, interactionType) => {
    const response = await fetch(`${API_BASE_URL}/pet/interact`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ pet_id: petId, interaction_type: interactionType }),
    });
    if (!response.ok) {
      throw new Error('Failed to interact with pet');
    }
    return response.json();
  },

  getUserWallet: async (userId) => {
    const response = await fetch(`${API_BASE_URL}/user/wallet/${userId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch user wallet');
    }
    return response.json();
  },
};

export default critterCraftAPI;