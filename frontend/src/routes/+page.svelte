<script>
  import { goto } from '$app/navigation';
</script>

<div
  class="hero min-h-screen"
  style="background-image: url(https://images.pexels.com/photos/176851/pexels-photo-176851.jpeg);"
>
  <div class="hero-overlay"></div>
  <div class="hero-content text-neutral-content text-center">
    <div class="max-w-md">
      <h1 class="mb-5 text-5xl font-bold">Ciao!</h1>
      <p class="mb-5">
        Welcome to our mini SaaS platform. Here you can login as a staff and enter an issue.
      </p>
      <button on:click={() => goto('/oauth')} class="btn btn-primary p-4 mx-4 rounded-lg">Get started</button>
    </div>
  </div>
  
  <!-- Staff login link in bottom right -->
  <div class="fixed bottom-4 right-4">
    <a href="/login" class="">
      
        
      Login as Staff
    </a>
  </div>
</div>