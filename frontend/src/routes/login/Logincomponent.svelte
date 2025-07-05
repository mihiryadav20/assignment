<script lang="ts">
  export let title = "Login now!";
  export let description = "Welcome to our mini SaaS platform. Here you can login as a staff and enter an issue.";

  interface UserData {
    email: string;
    [key: string]: any;
  }

  let email = "";
  let password = "";
  let isLoading = false;
  let errorMessage = "";
  let isLoggedIn = false;
  let userData: UserData | null = null;

  async function handleLogin() {
    isLoading = true;
    errorMessage = "";
    
    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || 'Login failed');
      }
      
      isLoggedIn = true;
      userData = data as UserData;
      console.log('Login successful:', data);
      
    } catch (error: unknown) {
      console.error('Login error:', error);
      errorMessage = error instanceof Error ? error.message : 'Failed to login. Please try again.';
    } finally {
      isLoading = false;
    }
  }

  function handleLogout() {
    isLoggedIn = false;
    userData = null;
  }
</script>

<div class="hero bg-base-200 min-h-screen">
  <div class="hero-content flex-col lg:flex-row-reverse">
    <div class="text-center lg:text-left">
      <h1 class="text-5xl font-bold">{title}</h1>
      <p class="py-6">{description}</p>
    </div>
    
    {#if isLoggedIn && userData}
      <div class="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl">
        <div class="card-body text-center">
          <h2 class="text-2xl font-bold">Welcome, {userData.email}!</h2>
          <p class="py-4">You have successfully logged in.</p>
          <button class="btn btn-primary" on:click={handleLogout}>Logout</button>
        </div>
      </div>
    {:else}
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
              
              <div class="divider">OR</div>
              
              <button 
                type="button" 
                class="btn btn-outline w-full"
              >
                <svg class="w-5 h-5 mr-2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                  <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                  <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
                  <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                </svg>
                Continue with Google
              </button>
            </fieldset>
          </form>
        </div>
      </div>
    {/if}
  </div>
</div>