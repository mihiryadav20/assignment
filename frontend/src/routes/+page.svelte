<script>
  import { goto } from '$app/navigation';
</script>

<div
  class="hero min-h-screen"
  style="background-image: url(https://cdn.midjourney.com/5056374d-8788-40fa-8747-95f988be43bb/0_3.png);"
>
  <div class="hero-overlay"></div>
  <div class="hero-content text-neutral-content text-center">
    <div class="max-w-md">
      <h1 class="mb-5 text-5xl font-bold">Ciao!</h1>
      <p class="mb-5">
        Welcome to our mini SaaS platform. Here you can login as a staff and enter an issue.
      </p>
      <button on:click={() => goto('/login')} class="btn btn-primary p-4 mx-4">Get started</button>
    </div>
  </div>
  
  <!-- Staff login link in bottom right -->
  <div class="fixed bottom-4 right-4">
    <a href="/login" class="btn btn-ghost">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
      </svg>
      Login as Staff
    </a>
  </div>
</div>