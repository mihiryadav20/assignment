import type { ApiError } from '$lib/models';

import { BaseUrl } from '$lib/url';

const API_BASE_URL = `${BaseUrl}/api`;

export async function apiFetch<T>(
  endpoint: string, 
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem('auth_token');
  
  const headers = new Headers(options.headers);
  headers.set('Content-Type', 'application/json');
  
  if (token) {
    headers.set('Authorization', `Token ${token}`);
  }
  
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
    credentials: 'include',
  });
  
  if (!response.ok) {
    const error: ApiError = {
      message: response.statusText,
      status: response.status
    };
    
    try {
      const errorData = await response.json();
      error.message = errorData.detail || errorData.message || response.statusText;
    } catch (e) {
      console.error('Error parsing error response:', e);
    }
    
    throw error;
  }
  
  // Handle empty responses (like 204 No Content)
  if (response.status === 204) {
    return undefined as unknown as T;
  }
  
  return response.json();
}
