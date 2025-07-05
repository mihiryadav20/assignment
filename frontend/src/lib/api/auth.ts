import type { User, AuthResponse, ApiError } from '$lib/models';
import { BaseUrl, ApiEndpoints } from '$lib/url';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error: ApiError = {
      message: response.statusText,
      status: response.status
    };
    
    try {
      const errorData = await response.json();
      error.message = errorData.detail || errorData.message || response.statusText;
    } catch (e) {
      // If we can't parse the error response, use the status text
      console.error('Error parsing error response:', e);
    }
    
    throw error;
  }
  
  return response.json();
}

export async function login(email: string, password: string): Promise<AuthResponse> {
  const response = await fetch(`${BaseUrl}${ApiEndpoints.auth.login}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include',
    body: JSON.stringify({ email, password })
  });
  
  return handleResponse<AuthResponse>(response);
}

export async function getCurrentUser(token: string): Promise<User> {
  const response = await fetch(`${BaseUrl}${ApiEndpoints.auth.user}`, {
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    },
    credentials: 'include'
  });
  
  const data = await handleResponse<User | { user: User }>(response);
  // If the response is { user: {...} }, return the user object, otherwise return the response as is
  if (data && typeof data === 'object' && 'user' in data) {
    return data.user;
  }
  return data as User;
}

export function logout(): void {
  localStorage.removeItem('auth_token');
  localStorage.removeItem('userData');
}
