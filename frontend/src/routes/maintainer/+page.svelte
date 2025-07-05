<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { getCurrentUser, logout } from '$lib/api';
  import type { User } from '$lib/models';
  
  let user: User | null = null;
  let isLoading = true;
  let errorMessage = "";

  onMount(async () => {
    const token = localStorage.getItem('auth_token');
    
    if (!token) {
      goto('/login');
      return;
    }
    
    try {
      user = await getCurrentUser(token);
      // Store user data in localStorage for quick access
      localStorage.setItem('userData', JSON.stringify(user));
    } catch (error: unknown) {
      console.error('Authentication error:', error);
      errorMessage = error instanceof Error ? error.message : 'Failed to load user data';
      logout();
      goto('/login');
    } finally {
      isLoading = false;
    }
  });
  
  function handleLogout() {
    logout();
    goto('/login');
  }
</script>

<div class="min-h-screen bg-base-200 p-4">
  <div class="navbar bg-base-100 rounded-lg shadow-md mb-6">
    <div class="flex-1">
      <h1 class="text-xl font-bold">Maintainer Dashboard</h1>
    </div>
    <div class="flex-none">
      <button on:click={handleLogout} class="btn btn-ghost">
        <span>Logout</span>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
      </button>
    </div>
  </div>
  
  {#if isLoading}
  <div class="flex justify-center items-center h-48">
    <span class="loading loading-spinner loading-lg"></span>
  </div>
{:else if errorMessage}
  <div class="alert alert-error shadow-lg mb-8">
    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
    <span>{errorMessage}</span>
  </div>
{:else if user}
  <div class="card bg-base-100 shadow-lg mb-6">
    <div class="card-body">
      <div class="flex justify-between items-start">
        <div>
          <h2 class="card-title text-2xl">Welcome, {user.first_name || user.username || 'User'}</h2>
          <p class="text-gray-500">Here's your account information</p>
        </div>
        <div class="badge badge-lg" class:badge-primary={user.role === 'Admin'} class:badge-secondary={user.role === 'Staff'}>
          {user.role || (user.is_superuser ? 'Admin' : user.is_staff ? 'Staff' : 'User')}
        </div>
      </div>
      <div class="divider my-2"></div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
        <div>
          <div class="text-sm text-gray-500">Email</div>
          <div class="font-medium">{user.email || 'N/A'}</div>
        </div>
        <div>
          <div class="text-sm text-gray-500">User ID</div>
          <div class="font-mono">{user.id || 'N/A'}</div>
        </div>
        <div>
          <div class="text-sm text-gray-500">Full Name</div>
          <div class="font-medium">
            {user.first_name || user.last_name 
              ? `${user.first_name || ''} ${user.last_name || ''}`.trim()
              : 'N/A'
            }
          </div>
        </div>
        <div>
          <div class="text-sm text-gray-500">Username</div>
          <div class="font-medium">{user.username || 'N/A'}</div>
        </div>
      </div>
    </div>
  </div>
{/if}
</div>