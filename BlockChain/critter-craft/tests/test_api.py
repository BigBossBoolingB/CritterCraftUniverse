import sys
import os
import json
import pytest

# Add the 'src' directory to the Python path to allow for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from api.app import app
from services import user_manager

@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def cleanup_mocks():
    """Reset the mock databases before each test."""
    user_manager.mock_users.clear()
    user_manager.mock_sessions.clear()

def test_register_success(client):
    """Test successful user registration."""
    response = client.post('/register', json={'username': 'testuser', 'password': 'password123'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True
    assert 'user_id' in data

def test_register_user_exists(client):
    """Test registration failure when user already exists."""
    client.post('/register', json={'username': 'testuser', 'password': 'password123'})
    response = client.post('/register', json={'username': 'testuser', 'password': 'password123'})
    assert response.status_code == 409
    assert response.get_json()['success'] is False

def test_login_success(client):
    """Test successful user login."""
    client.post('/register', json={'username': 'testuser', 'password': 'password123'})
    response = client.post('/login', json={'username': 'testuser', 'password': 'password123'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'session_token' in data
    assert 'session_token' in response.headers['Set-Cookie']

def test_login_invalid_credentials(client):
    """Test login failure with invalid credentials."""
    client.post('/register', json={'username': 'testuser', 'password': 'password123'})
    response = client.post('/login', json={'username': 'testuser', 'password': 'wrongpassword'})
    assert response.status_code == 401
    assert response.get_json()['success'] is False

def test_validate_session_success(client):
    """Test successful session validation."""
    client.post('/register', json={'username': 'testuser', 'password': 'password123'})
    login_response = client.post('/login', json={'username': 'testuser', 'password': 'password123'})
    session_token = login_response.get_json()['session_token']

    # Test validation using JSON body
    response = client.post('/validate_session', json={'session_token': session_token})
    assert response.status_code == 200
    assert response.get_json()['success'] is True

    # Test validation using cookie
    response = client.post('/validate_session', json={})
    assert response.status_code == 200
    assert response.get_json()['success'] is True


def test_validate_session_invalid(client):
    """Test session validation failure with an invalid token."""
    response = client.post('/validate_session', json={'session_token': 'invalid_token'})
    assert response.status_code == 401
    assert response.get_json()['success'] is False

def test_logout_success(client):
    """Test successful user logout."""
    client.post('/register', json={'username': 'testuser', 'password': 'password123'})
    login_response = client.post('/login', json={'username': 'testuser', 'password': 'password123'})
    session_token = login_response.get_json()['session_token']

    response = client.post('/logout', json={'session_token': session_token})
    assert response.status_code == 200
    assert response.get_json()['success'] is True
    assert 'session_token=;' in response.headers['Set-Cookie']

    # Verify session is no longer valid
    validate_response = client.post('/validate_session', json={'session_token': session_token})
    assert validate_response.status_code == 401

def test_get_public_key_success(client):
    """Test successfully retrieving a user's public key."""
    reg_response = client.post('/register', json={'username': 'testuser', 'password': 'password123'})
    user_id = reg_response.get_json()['user_id']

    response = client.get(f'/get_public_key/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'public_key' in data
    assert data['public_key'] == f'pub_key_for_{user_id}'

def test_get_public_key_not_found(client):
    """Test failure when retrieving a public key for a non-existent user."""
    response = client.get('/get_public_key/non_existent_user_id')
    assert response.status_code == 404
    assert response.get_json()['success'] is False

def test_get_user_profile_success(client):
    """Test successful retrieval of user profile."""
    reg_response = client.post('/register', json={'username': 'testuser', 'password': 'password123'})
    user_id = reg_response.get_json()['user_id']

    login_response = client.post('/login', json={'username': 'testuser', 'password': 'password123'})
    token = login_response.get_json()['session_token']

    response = client.get('/api/user/profile', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['profile']['user_id'] == user_id
    assert data['profile']['username'] == 'testuser'

def test_get_user_profile_no_token(client):
    """Test failure when no token is provided for profile retrieval."""
    response = client.get('/api/user/profile')
    assert response.status_code == 401
    assert response.get_json()['success'] is False
