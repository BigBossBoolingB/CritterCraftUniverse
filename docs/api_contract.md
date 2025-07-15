# CritterCraftUniverse API Contract

This document defines the API contract for the CritterCraftUniverse application.

## 1. Pet API

### 1.1. Get Pet Status

*   **Endpoint:** `GET /api/pet/status/<pet_id>`
*   **Description:** Retrieves the current status of a pet.
*   **Response:**
    ```json
    {
      "id": "string",
      "name": "string",
      "species": "string",
      "aura_color": "string",
      "mood": "string",
      "hunger": "integer",
      "happiness": "integer",
      "energy": "integer",
      "personality_traits": {
        "playfulness": "integer",
        "curiosity": "integer",
        "sociability": "integer",
        "independence": "integer",
        "loyalty": "integer"
      }
    }
    ```

### 1.2. Interact with Pet

*   **Endpoint:** `POST /api/pet/interact`
*   **Description:** Sends an interaction to a pet.
*   **Request Body:**
    ```json
    {
      "pet_id": "string",
      "interaction_type": "string"
    }
    ```
*   **Response:**
    ```json
    {
      "success": "boolean",
      "message": "string"
    }
    ```

## 2. User API

### 2.1. Get User Wallet

*   **Endpoint:** `GET /api/user/wallet/<user_id>`
*   **Description:** Retrieves a user's wallet information.
*   **Response:**
    ```json
    {
      "qrasl_balance": "integer"
    }
    ```
