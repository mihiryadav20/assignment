<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  
  // Define user interface
  interface User {
    name?: string;
    first_name?: string;
    last_name?: string;
    email?: string;
    [key: string]: any; // For any additional fields
  }
  
  let user: User | null = null;
  let isLoading = true;
  let errorMessage = "";
  
  // Form data
  let title = "";
  let description = "";
  let attachment: File | null = null;
  let isSubmitting = false;
  let submitSuccess = false;
  let submitError = "";
  
  // Function to handle logout
  async function handleLogout() {
    try {
      // Call Django logout endpoint
      await fetch('http://localhost:8000/api/auth/logout/', {
        method: 'POST',
        credentials: 'include'
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear local storage
      localStorage.removeItem('userData');
      goto('/');
    }
  }
  
  // Function to handle form submission
  async function handleSubmit() {
    if (!title || !description) {
      submitError = "Please fill in all required fields";
      return;
    }
    
    isSubmitting = true;
    submitError = "";
    submitSuccess = false;
    
    try {
      // First, get a CSRF token by making a GET request to the server
      const tokenResponse = await fetch('http://localhost:8000/api/auth/user/', {
        method: 'GET',
        credentials: 'include'
      });
      
      if (!tokenResponse.ok) {
        throw new Error('Failed to authenticate with the server');
      }
      
      // Create FormData object
      const formData = new FormData();
      formData.append('title', title);
      formData.append('description', description);
      if (attachment) {
        formData.append('attachment', attachment);
      }
      
      // Use XMLHttpRequest instead of fetch for better CORS handling with file uploads
      const xhr = new XMLHttpRequest();
      
      // Create a Promise to handle the XHR request
      const requestPromise = new Promise((resolve, reject) => {
        xhr.open('POST', 'http://localhost:8000/api/issues/create/', true);
        xhr.withCredentials = true; // Include credentials
        
        xhr.onload = function() {
          if (xhr.status >= 200 && xhr.status < 300) {
            resolve(xhr.response);
          } else {
            try {
              const errorData = JSON.parse(xhr.responseText);
              reject(new Error(errorData.message || errorData.detail || `Error ${xhr.status}: ${xhr.statusText}`));
            } catch (e) {
              reject(new Error(`Error ${xhr.status}: ${xhr.statusText}`));
            }
          }
        };
        
        xhr.onerror = function() {
          reject(new Error('Network error occurred'));
        };
        
        // Send the FormData
        xhr.send(formData);
      });
      
      // Wait for the request to complete
      await requestPromise;
      
      // Reset form on success
      title = "";
      description = "";
      attachment = null;
      submitSuccess = true;
    } catch (error) {
      console.error('Error submitting issue:', error);
      submitError = error instanceof Error ? error.message : 'An unknown error occurred';
    } finally {
      isSubmitting = false;
    }
  }
  
  // Handle file input change
  function handleFileChange(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      attachment = input.files[0];
    } else {
      attachment = null;
    }
  }
  
  onMount(async () => {
    try {
      // First check if we have user data in localStorage
      const userData = localStorage.getItem('userData');
      if (userData) {
        user = JSON.parse(userData);
        isLoading = false;
        return;
      }
      
      // If not, try to fetch from Django session
      const response = await fetch('http://localhost:8000/api/auth/user/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      });
      
      if (!response.ok) {
        throw new Error('Not authenticated');
      }
      
      // Get user data
      const data = await response.json();
      user = data;
      
      // Store in localStorage
      localStorage.setItem('userData', JSON.stringify(data));
    } catch (error) {
      console.error('Authentication error:', error);
      errorMessage = 'You are not authenticated. Please log in.';
      goto('/oauth');
    } finally {
      isLoading = false;
    }
  });
  
  // Function to fetch user data from API if needed - not used anymore
  async function fetchUserData(token: string) {
    try {
      const response = await fetch('http://localhost:8000/api/auth/user/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch user data');
      }
      
      const userData = await response.json();
      user = userData;
      localStorage.setItem('userData', JSON.stringify(userData));
    } catch (error) {
      console.error('Error fetching user data:', error);
      errorMessage = 'Failed to fetch user data. Please try logging in again.';
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="min-h-screen bg-base-200 p-4">
  <div class="navbar bg-base-100 rounded-box mb-6">
    <div class="flex-1">
      <a href="/" class="btn btn-ghost normal-case text-xl">DeepLogic</a>
    </div>
    <div class="flex-none">
      <button class="btn btn-ghost" on:click={handleLogout}>
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
        Logout
      </button>
    </div>
  </div>
  
  {#if isLoading}
    <div class="flex justify-center items-center py-8">
      <span class="loading loading-spinner loading-lg"></span>
      <span class="ml-2">Loading user data...</span>
    </div>
  {:else if errorMessage}
    <div class="alert alert-error">
      <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
      <span>{errorMessage}</span>
    </div>
    <div class="text-center mt-4">
      <button class="btn btn-primary" on:click={() => goto('/oauth')}>Return to Login</button>
    </div>
  {:else if user}
    <div class="card bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title text-2xl mb-6">Here you can report an issue</h2>
        
        <div class="bg-base-200 rounded-box p-6 mb-6">
          <h3 class="text-xl font-bold mb-4">Your Profile</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <div class="stat">
                <div class="stat-title">Name</div>
                <div class="stat-value text-lg">{user.name || user.first_name + ' ' + user.last_name || 'N/A'}</div>
              </div>
            </div>
            
            <div>
              <div class="stat">
                <div class="stat-title">Email</div>
                <div class="stat-value text-lg">{user.email || 'N/A'}</div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Issue Submission Form -->
        <div class="bg-base-200 rounded-box p-6 mb-6">
          <h3 class="text-xl font-bold mb-4">Submit New Issue</h3>
          
          <form on:submit|preventDefault={handleSubmit} class="space-y-4">
            <!-- Title Input -->
            <div class="form-control w-full">
              <label class="label" for="title">
                <span class="label-text font-medium">Issue Title <span class="text-red-500">*</span></span>
              </label>
              <input 
                type="text" 
                id="title"
                bind:value={title} 
                placeholder="Enter a descriptive title" 
                class="input input-bordered w-full" 
                required
              />
            </div>
            
            <!-- Description Input -->
            <fieldset class="fieldset w-full">
              <legend class="fieldset-legend">Description <span class="text-red-500">*</span></legend>
              <textarea 
                id="description"
                bind:value={description}
                placeholder="Provide detailed information about the issue"
                class="textarea h-24 textarea-bordered w-full"
                required
              ></textarea>
            </fieldset>
            
            <!-- File Attachment -->
            <div class="form-control w-full">
              <label class="label" for="attachment">
                <span class="label-text font-medium">Attachment</span>
                <span class="label-text-alt">Optional</span>
              </label>
              <input 
                type="file" 
                id="attachment"
                on:change={handleFileChange} 
                class="file-input file-input-bordered w-full" 
              />
              {#if attachment}
                <p class="text-sm mt-2">Selected file: {attachment.name} ({Math.round(attachment.size / 1024)} KB)</p>
              {/if}
            </div>
            
            <!-- Submit Button -->
            <div class="form-control mt-6">
              <button 
                type="submit" 
                class="btn btn-primary" 
                disabled={isSubmitting}
              >
                {#if isSubmitting}
                  <span class="loading loading-spinner loading-sm mr-2"></span>
                  Submitting...
                {:else}
                  Submit Issue
                {/if}
              </button>
            </div>
            
            <!-- Success Message -->
            {#if submitSuccess}
              <div class="alert alert-success mt-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>Issue submitted successfully!</span>
              </div>
            {/if}
            
            <!-- Error Message -->
            {#if submitError}
              <div class="alert alert-error mt-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>{submitError}</span>
              </div>
            {/if}
          </form>
        </div>
      </div>
    </div>
  {:else}
    <div class="alert alert-warning">
      <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
      <span>No user data found. Please log in again.</span>
    </div>
    <div class="text-center mt-4">
      <button class="btn btn-primary" on:click={() => goto('/oauth')}>Go to Login</button>
    </div>
  {/if}
</div>