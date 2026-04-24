const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export const fetchUsers = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/users`);
    if (!response.ok) {
      throw new Error('Failed to fetch users');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching users:', error);
    return [];
  }
};

export const fetchSongs = async () => {
  try {
    // Note: This endpoint might require auth. Using a placeholder for auth token if needed.
    const token = localStorage.getItem('token') || ''; 
    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { 'x-auth-token': token } : {})
    };
    
    const response = await fetch(`${API_BASE_URL}/songs/all`, { headers });
    if (!response.ok) {
      throw new Error('Failed to fetch songs');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching songs:', error);
    return [];
  }
};
