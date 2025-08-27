"""
Placeholder for User Management Service.

This module will contain the business logic for user registration,
authentication, session management, and key management.
"""

import uuid
from datetime import datetime, timedelta, timezone

# Mock database for users and sessions
# In a real implementation, this would be a database connection.
mock_users = {}
mock_sessions = {}

def register(username, password):
    """
    Registers a new user.
    In a real implementation, this would hash the password and store it in a database.
    """
    if username in mock_users:
        return {"success": False, "message": "User already exists"}, 409

    user_id = str(uuid.uuid4())
    mock_users[username] = {
        "user_id": user_id,
        "password": password, # In a real app, NEVER store plain text passwords
        "public_key": f"pub_key_for_{user_id}"
    }
    return {"success": True, "message": "User registered successfully", "user_id": user_id}, 201

def login(username, password):
    """
    Logs a user in and creates a session.
    """
    user = mock_users.get(username)
    if user and user["password"] == password:
        session_token = str(uuid.uuid4())
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        mock_sessions[session_token] = {
            "user_id": user["user_id"],
            "expires_at": expires_at
        }
        return {"success": True, "message": "Login successful", "session_token": session_token}, 200
    return {"success": False, "message": "Invalid credentials"}, 401

def validate_session(session_token):
    """
    Validates a session token.
    """
    session = mock_sessions.get(session_token)
    if session and session["expires_at"] > datetime.now(timezone.utc):
        return {"success": True, "user_id": session["user_id"]}, 200
    return {"success": False, "message": "Invalid or expired session"}, 401

def logout(session_token):
    """
    Logs a user out by deleting their session.
    """
    if session_token in mock_sessions:
        del mock_sessions[session_token]
        return {"success": True, "message": "Logout successful"}, 200
    return {"success": False, "message": "Invalid session token"}, 404

def get_public_key(user_id):
    """
    Retrieves a user's public key.
    """
    for user in mock_users.values():
        if user["user_id"] == user_id:
            return {"success": True, "public_key": user["public_key"]}, 200
    return {"success": False, "message": "User not found"}, 404

def get_user_profile(user_id):
    """
    Retrieves a user's profile data.
    """
    for username, user_data in mock_users.items():
        if user_data["user_id"] == user_id:
            return {
                "success": True,
                "profile": {
                    "user_id": user_id,
                    "username": username,
                    "public_key": user_data["public_key"]
                }
            }, 200
    return {"success": False, "message": "User not found"}, 404

def update_user_profile(user_id, new_data):
    """
    Updates a user's profile data.
    For now, only allows updating the username.
    """
    old_username = None
    for username, user_data in mock_users.items():
        if user_data["user_id"] == user_id:
            old_username = username
            break

    if not old_username:
        return {"success": False, "message": "User not found"}, 404

    new_username = new_data.get("username")
    if not new_username:
        return {"success": False, "message": "No new username provided"}, 400

    if new_username != old_username and new_username in mock_users:
        return {"success": False, "message": "Username already taken"}, 409

    # In-memory update by removing old and adding new
    user_record = mock_users.pop(old_username)
    mock_users[new_username] = user_record

    # Placeholder for publishing event to Identity Event Stream
    print(f"EVENT: User profile updated for user_id {user_id}. Username changed from {old_username} to {new_username}")

    return {"success": True, "message": "Profile updated successfully"}, 200
