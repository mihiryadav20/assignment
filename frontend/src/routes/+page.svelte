<div class="container mx-auto p-4">
  <h1 class="text-4xl font-bold mb-6">Cyberpunk Theme Demo</h1>
  
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
    <div class="card bg-base-200 shadow-xl">
      <div class="card-body">
        <h2 class="card-title">Cyberpunk UI Components</h2>
        <p>This card demonstrates the cyberpunk theme from DaisyUI.</p>
        <div class="card-actions justify-end mt-4">
          <button class="btn btn-primary">Primary</button>
          <button class="btn btn-secondary">Secondary</button>
          <button class="btn btn-accent">Accent</button>
        </div>
      </div>
    </div>
    
    <div class="card bg-base-300 shadow-xl">
      <div class="card-body">
        <h2 class="card-title">More Components</h2>
        <div class="form-control w-full max-w-xs">
          <label class="label" for="name-input">
            <span class="label-text">Enter your name</span>
          </label>
          <input type="text" id="name-input" placeholder="Type here" class="input input-bordered w-full max-w-xs" />
        </div>
        <div class="mt-4">
          <div class="badge badge-primary mr-2">Primary</div>
          <div class="badge badge-secondary mr-2">Secondary</div>
          <div class="badge badge-accent">Accent</div>
        </div>
      </div>
    </div>
  </div>
  
  <div class="flex flex-col gap-4">
    <progress class="progress progress-primary w-full" value="40" max="100"></progress>
    <progress class="progress progress-secondary w-full" value="70" max="100"></progress>
    <div class="alert alert-info">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
      <span>This is using the cyberpunk theme from DaisyUI.</span>
    </div>
  </div>
  
  <div class="mt-8">
    <a href="https://svelte.dev/docs/kit" class="link link-primary">Learn more about SvelteKit</a>
  </div>
</div>
