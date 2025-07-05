<script lang="ts">
  import { goto } from '$app/navigation';
  
  export let title = "Login now!";
  export let description = "Welcome to our mini SaaS platform. Here you can login as a staff and enter an issue.";

  let email = "";
  let password = "";
  let isLoading = false;
  let errorMessage = "";


  async function handleLogin() {
    isLoading = true;
    errorMessage = "";
    
    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({ email, password })
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || 'Login failed');
      }
      
      const data = await response.json();
      
      // Store the token in localStorage
      if (data.token) {
        localStorage.setItem('auth_token', data.token);
        // Store user data in localStorage
        localStorage.setItem('userData', JSON.stringify(data));
        // Redirect to maintainer page after successful login
        goto('/maintainer');
      } else {
        throw new Error('No authentication token received');
      }
      
    } catch (error) {
      console.error('Login error:', error);
      errorMessage = error instanceof Error ? error.message : 'Failed to login. Please try again.';
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="hero bg-base-200 min-h-screen">
  <div class="hero-content flex-col lg:flex-row-reverse">
    <div class="text-center lg:text-left">
      <h1 class="text-5xl font-bold">{title}</h1>
      <p class="py-6">{description}</p>
    </div>
    
    <div class="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl">
        <div class="card-body">
          {#if errorMessage}
            <div class="alert alert-error">
              <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              <span>{errorMessage}</span>
            </div>
          {/if}
          

          
          <form on:submit|preventDefault={handleLogin}>
            <fieldset class="fieldset">
              <label class="label" for="email">Email</label>
              <input 
                id="email"
                type="email" 
                class="input input-bordered w-full" 
                placeholder="Email" 
                bind:value={email}
                required
              />
              
              <label class="label" for="password">Password</label>
              <input 
                id="password"
                type="password" 
                class="input input-bordered w-full" 
                placeholder="Password" 
                bind:value={password}
                required
              />
              
              <button 
                type="submit" 
                class="btn btn-neutral mt-4 w-full" 
                disabled={isLoading}
              >
                {#if isLoading}
                  <span class="loading loading-spinner loading-sm"></span>
                  Signing in...
                {:else}
                  Login
                {/if}
              </button>
            </fieldset>
          </form>
        </div>
      </div>
  </div>
</div>