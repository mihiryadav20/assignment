<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  let isLoading = true;
  let errorMessage = "";
  
  // Function to check if user is already authenticated
  async function checkUserSession() {
    try {
      // Try to get user info from Django session
      const response = await fetch('http://localhost:8000/api/auth/user/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      });
      
      if (response.ok) {
        // User is already authenticated
        const userData = await response.json();
        console.log('User already authenticated:', userData);
        
        // Store user data
        localStorage.setItem('userData', JSON.stringify(userData));
        
        // Redirect to reporter page
        goto('/reporter');
        return;
      }
    } catch (error) {
      console.log('Not authenticated yet, showing login page');
    } finally {
      isLoading = false;
    }
  }
  
  // Function to initiate OAuth login
  function initiateOAuth() {
    // Store the return URL in localStorage
    localStorage.setItem('oauth_return_url', '/reporter');
    
    // Redirect to Django's Google OAuth endpoint
    window.location.href = 'http://localhost:8000/auth/login/google-oauth2/';
  }
  
  onMount(() => {
    // Check if user is already authenticated
    checkUserSession();
  });
</script>

<div class="min-h-screen flex items-center justify-center bg-base-200">
  <div class="card w-96 bg-base-100 shadow-xl">
    <div class="card-body">
      <h2 class="card-title text-2xl font-bold mb-4">Authentication</h2>
      
      {#if isLoading}
        <div class="flex flex-col items-center justify-center py-8">
          <span class="loading loading-spinner loading-lg"></span>
          <p class="mt-4">Processing authentication...</p>
        </div>
      {:else if errorMessage}
        <div class="alert alert-error mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <span>{errorMessage}</span>
        </div>
        <button class="btn btn-primary w-full" on:click={() => initiateOAuth()}>Try Again</button>
      {:else}
        <p class="mb-6">Click the button below to sign in with your Google account.</p>
        <button class="btn btn-primary w-full" on:click={() => initiateOAuth()}>
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="mr-2"><path fill="currentColor" d="M12.545 10.239v3.821h5.445c-.712 2.315-2.647 3.972-5.445 3.972a6.033 6.033 0 110-12.064c1.498 0 2.866.549 3.921 1.453l2.814-2.814A9.969 9.969 0 0012.545 2C7.021 2 2.543 6.477 2.543 12s4.478 10 10.002 10c8.396 0 10.249-7.85 9.426-11.748l-9.426-.013z"/></svg>
          Sign in with Google
        </button>
      {/if}
      
      <div class="mt-4 text-center">
        <a href="/" class="link link-hover">Back to Home</a>
      </div>
    </div>
  </div>
</div>