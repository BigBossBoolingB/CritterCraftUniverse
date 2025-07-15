# Development Setup

This document describes how to set up the development environment for CritterCraftUniverse.

## Prerequisites

*   Node.js and npm
*   Python and pip
*   Flask

## Running the Application

1.  **Start the backend server:**
    ```bash
    cd BlockChain/pet
    python main.py
    ```

2.  **Start the frontend development server:**
    ```bash
    cd frontend
    npm install
    npm start
    ```

3.  **Configure proxy settings:**
    In `frontend/package.json`, add the following line:
    ```json
    "proxy": "http://localhost:5000"
    ```
