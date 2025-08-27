/**
 * API Client for the CritterCraft RESTful API.
 *
 * This module provides functions for interacting with the user authentication
 * and session management endpoints of the backend server.
 */

const API_BASE_URL = 'http://127.0.0.1:5000'; // The address of the Flask server

/**
 * A helper function to handle fetch requests and responses.
 * @param {string} url - The URL to fetch.
 * @param {object} options - The options for the fetch request.
 * @returns {Promise<object>} - The JSON response from the server.
 * @throws {Error} - If the network response is not ok.
 */
const fetchAPI = async (url, options = {}) => {
  const response = await fetch(url, options);

  if (!response.ok) {
    let errorMessage = `HTTP error! status: ${response.status}`;
    try {
      const errorBody = await response.json();
      errorMessage = errorBody.message || errorMessage;
    } catch (e) {
      // Ignore if response is not JSON
    }
    throw new Error(errorMessage);
  }

  // For 204 No Content, there is no body to parse
  if (response.status === 204) {
    return null;
  }

  return response.json();
};

/**
 * Registers a new user.
 * @param {string} username - The username for the new user.
 * @param {string} password - The password for the new user.
 * @returns {Promise<object>} - The server response.
 */
export const register = async (username, password) => {
  return fetchAPI(`${API_BASE_URL}/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  });
};

/**
 * Logs in a user.
 * @param {string} username - The user's username.
 * @param {string} password - The user's password.
 * @returns {Promise<object>} - The server response, including the session token.
 */
export const login = async (username, password) => {
  const data = await fetchAPI(`${API_BASE_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  });

  // Store the token upon successful login
  if (data && data.session_token) {
    localStorage.setItem('session_token', data.session_token);
  }

  return data;
};

/**
 * Validates the current session token.
 * @returns {Promise<object>} - The server response.
 */
export const validateSession = async () => {
  const token = localStorage.getItem('session_token');
  if (!token) {
    return Promise.reject(new Error('No session token found.'));
  }

  return fetchAPI(`${API_BASE_URL}/validate_session`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ session_token: token }),
  });
};

/**
 * Logs out the current user.
 * @returns {Promise<void>}
 */
export const logout = async () => {
  const token = localStorage.getItem('session_token');
  if (!token) {
    return Promise.resolve();
  }

  try {
    await fetchAPI(`${API_BASE_URL}/logout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ session_token: token }),
    });
  } finally {
    // Always remove the token from local storage, even if the server call fails
    localStorage.removeItem('session_token');
  }
};

/**
 * Fetches the user profile data.
 * @returns {Promise<object>} - The user's profile data.
 */
export const getUserProfile = async () => {
  const token = localStorage.getItem('session_token');
  if (!token) {
    return Promise.reject(new Error('No session token found.'));
  }

  return fetchAPI(`${API_BASE_URL}/api/user/profile`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
  });
};

/**
 * Updates the user profile data.
 * @param {object} profileData - The new profile data.
 * @returns {Promise<object>} - The server response.
 */
export const updateUserProfile = async (profileData) => {
  const token = localStorage.getItem('session_token');
  if (!token) {
    return Promise.reject(new Error('No session token found.'));
  }

  return fetchAPI(`${API_BASE_URL}/api/user/profile`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(profileData),
  });
};
