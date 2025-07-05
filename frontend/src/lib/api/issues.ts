import { BaseUrl, ApiEndpoints } from '$lib/url';
import type { ApiError } from '$lib/models';
import { apiFetch } from './client';

// Define the Issue interface based on the actual API response
export interface Issue {
  id: string;
  title: string;
  description: string;
  status: string;
  status_display: string;
  severity: string;
  severity_display: string;
  created_by: {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    role: string;
  };
  created_at: string;
  updated_at: string;
  attachment?: string;
  attachment_name?: string;
}

/**
 * Fetch all issues from the API
 */
export async function getIssues(): Promise<Issue[]> {
  return apiFetch<Issue[]>(ApiEndpoints.issues);
}

/**
 * Fetch a specific issue by ID
 */
export async function getIssueById(id: number): Promise<Issue> {
  return apiFetch<Issue>(`${ApiEndpoints.issues}${id}/`);
}

/**
 * Create a new issue
 */
export async function createIssue(issue: Omit<Issue, 'id' | 'created_at' | 'updated_at'>): Promise<Issue> {
  return apiFetch<Issue>(ApiEndpoints.issues, {
    method: 'POST',
    body: JSON.stringify(issue)
  });
}

/**
 * Update an existing issue
 */
export async function updateIssue(id: number, issue: Partial<Issue>): Promise<Issue> {
  return apiFetch<Issue>(`${ApiEndpoints.issues}${id}/`, {
    method: 'PATCH',
    body: JSON.stringify(issue)
  });
}

/**
 * Delete an issue
 */
export async function deleteIssue(id: number): Promise<void> {
  return apiFetch<void>(`${ApiEndpoints.issues}${id}/`, {
    method: 'DELETE'
  });
}
