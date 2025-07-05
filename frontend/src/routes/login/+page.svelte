<script lang="ts">
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
</script>

<div class="hero bg-base-200 min-h-screen">
  <div class="hero-content flex-col lg:flex-row-reverse">
    <div class="text-center lg:text-left">
      <h1 class="text-5xl font-bold">Login now!</h1>
      <p class="py-6">
        Welcome to our mini SaaS platform. Here you can login as a staff and enter an issue.
      </p>
    </div>
    
    {#if isLoggedIn && userData}
      <div class="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl">
        <div class="card-body text-center">
          <h2 class="text-2xl font-bold">Welcome, {userData.email}!</h2>
          <p class="py-4">You have successfully logged in.</p>
          <button class="btn btn-primary" on:click={() => { isLoggedIn = false; userData = null; }}>
            Logout
          </button>
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
              
              <div><a href="/forgot-password" class="link link-hover">Forgot password?</a></div>
              
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
    {/if}
  </div>
</div>