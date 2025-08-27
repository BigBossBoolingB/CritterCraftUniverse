"""
Main Flask application for the CritterCraft API.
"""

import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# This is a common pattern to make sure the application can find its modules
# when run from different directories.
# We add the 'src' directory to the Python path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services import user_manager

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for all routes

@app.route("/register", methods=["POST"])
def register():
    """
    User registration endpoint.
    Expects a JSON payload with "username" and "password".
    """
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"success": False, "message": "Missing username or password"}), 400

    username = data["username"]
    password = data["password"]

    response, status_code = user_manager.register(username, password)
    return jsonify(response), status_code

@app.route("/login", methods=["POST"])
def login():
    """
    User login endpoint.
    Expects a JSON payload with "username" and "password".
    Returns a session token on successful login.
    """
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"success": False, "message": "Missing username or password"}), 400

    username = data["username"]
    password = data["password"]

    response, status_code = user_manager.login(username, password)

    if status_code == 200:
        resp = jsonify(response)
        # In a real app, use secure, HttpOnly cookies
        resp.set_cookie('session_token', response['session_token'], httponly=True, samesite='Lax')
        return resp, status_code

    return jsonify(response), status_code

@app.route("/validate_session", methods=["POST"])
def validate_session():
    """
    Session validation endpoint.
    Expects a JSON payload with "session_token".
    """
    data = request.get_json()
    if not data or "session_token" not in data:
        # Fallback to checking cookies if not in JSON body
        token = request.cookies.get('session_token')
        if not token:
            return jsonify({"success": False, "message": "Missing session_token"}), 400
        data = {"session_token": token}

    session_token = data["session_token"]

    response, status_code = user_manager.validate_session(session_token)
    return jsonify(response), status_code

@app.route("/logout", methods=["POST"])
def logout():
    """
    User logout endpoint.
    Expects a JSON payload with "session_token".
    """
    data = request.get_json()
    if not data or "session_token" not in data:
        token = request.cookies.get('session_token')
        if not token:
            return jsonify({"success": False, "message": "Missing session_token"}), 400
        data = {"session_token": token}

    session_token = data["session_token"]

    response, status_code = user_manager.logout(session_token)

    if status_code == 200:
        resp = jsonify(response)
        resp.delete_cookie('session_token')
        return resp, status_code

    return jsonify(response), status_code

@app.route("/get_public_key/<string:user_id>", methods=["GET"])
def get_public_key(user_id):
    """
    Public key retrieval endpoint.
    Takes user_id from the URL path.
    """
    response, status_code = user_manager.get_public_key(user_id)
    return jsonify(response), status_code

@app.route("/api/user/profile", methods=["GET"])
def get_user_profile():
    """
    User profile retrieval endpoint.
    Requires a valid session token.
    """
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

    if not token:
        return jsonify({"success": False, "message": "Missing authentication token"}), 401

    validation_response, validation_status = user_manager.validate_session(token)

    if validation_status != 200:
        return jsonify(validation_response), validation_status

    user_id = validation_response["user_id"]

    profile_response, profile_status = user_manager.get_user_profile(user_id)

    return jsonify(profile_response), profile_status

# The following is not strictly necessary if using a WSGI server like Gunicorn/uWSGI
# but it's useful for direct script execution and local development.
if __name__ == '__main__':
    # Note: In a production environment, use a proper WSGI server.
    # The development server is not suitable for production.
    app.run(debug=True, port=5000)
