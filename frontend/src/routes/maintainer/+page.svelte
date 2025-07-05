<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { getCurrentUser, logout, getIssues, updateIssue } from '$lib/api';
  import type { User } from '$lib/models';
  import type { Issue } from '$lib/api/issues';
  
  let user: User | null = null;
  let issues: Issue[] = [];
  let isLoading = true;
  let isLoadingIssues = false;
  let errorMessage = "";
  let issuesError = "";
  let updateError = "";
  let isUpdating = false;
  let activeIssue: { id: string, field: string } | null = null;
  
  
  // Filtering
  let statusFilter = "all";
  let severityFilter = "all";
  let searchQuery = "";
  
  const statusOptions = ["all", "OPEN", "TRIAGED", "IN_PROGRESS", "DONE"];
  const severityOptions = ["all", "LOW", "MEDIUM", "HIGH", "CRITICAL"];

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
      
      // After authentication succeeds, load data
      await loadIssues();
    } catch (error: unknown) {
      console.error('Authentication error:', error);
      errorMessage = error instanceof Error ? error.message : 'Failed to load user data';
      logout();
      goto('/login');
    } finally {
      isLoading = false;
    }
  });
  
  async function loadIssues() {
    isLoadingIssues = true;
    issuesError = "";
    
    try {
      issues = await getIssues();
    } catch (error: unknown) {
      console.error('Error loading issues:', error);
      issuesError = error instanceof Error ? error.message : 'Failed to load issues';
    } finally {
      isLoadingIssues = false;
    }
  }
  
  // Handle updating issue status or severity
  async function handleUpdateIssue(issueId: string, field: 'status' | 'severity', value: string) {
    isUpdating = true;
    updateError = "";
    activeIssue = { id: issueId, field };
    
    try {
      // Create update payload with only the field being updated
      const updateData = field === 'status' 
        ? { status: value } 
        : { severity: value };
      
      // Call API to update the issue
      await updateIssue(issueId, updateData);
      
      // Refresh issues list to get updated data
      await loadIssues();
      
      // Show success message (optional)
      const toast = document.getElementById('update-toast');
      if (toast) {
        toast.classList.remove('hidden');
        setTimeout(() => toast.classList.add('hidden'), 3000);
      }
    } catch (error: unknown) {
      console.error(`Error updating issue ${field}:`, error);
      updateError = error instanceof Error ? error.message : `Failed to update issue ${field}`;
    } finally {
      isUpdating = false;
      activeIssue = null;
    }
  }
  
  
  function handleLogout() {
    logout();
    goto('/login');
  }
  
  // Filter issues based on status, severity, and search query
  $: filteredIssues = issues.filter(issue => {
    // Filter by status
    if (statusFilter !== 'all' && issue.status !== statusFilter) {
      return false;
    }
    
    // Filter by severity
    if (severityFilter !== 'all' && issue.severity !== severityFilter) {
      return false;
    }
    
    // Filter by search query
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      return (
        issue.title.toLowerCase().includes(query) ||
        issue.description.toLowerCase().includes(query) ||
        (issue.created_by.first_name && issue.created_by.first_name.toLowerCase().includes(query)) ||
        (issue.created_by.last_name && issue.created_by.last_name.toLowerCase().includes(query)) ||
        (issue.created_by.email && issue.created_by.email.toLowerCase().includes(query))
      );
    }
    
    return true;
  });
  
  // Format date to a more readable format
  function formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleString();
  }
  
  // Get appropriate badge class based on status
  function getStatusBadgeClass(status: string): string {
    switch (status) {
      case 'OPEN':
        return 'badge-primary';
      case 'TRIAGED':
        return 'badge-info';
      case 'IN_PROGRESS':
        return 'badge-warning';
      case 'DONE':
        return 'badge-success';
      default:
        return 'badge-ghost';
    }
  }
  
  // Get appropriate badge class based on severity
  function getSeverityBadgeClass(severity: string): string {
    switch (severity) {
      case 'LOW':
        return 'badge-info';
      case 'MEDIUM':
        return 'badge-warning';
      case 'HIGH':
        return 'badge-error';
      case 'CRITICAL':
        return 'badge-error text-white';
      default:
        return 'badge-ghost';
    }
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
          <h2 class="card-title text-2xl">Welcome, {(user.first_name && user.last_name) ? `${user.first_name} ${user.last_name}` : user.first_name || user.username || 'User'}</h2>
          <p class="text-gray-500">Here's your account information</p>
        </div>
        <div class="badge badge-lg" class:badge-primary={user.role === 'Admin'} class:badge-secondary={user.role === 'Staff'}>
          {user.role || (user.is_superuser ? 'Admin' : user.is_staff ? 'Staff' : 'User')}
        </div>
      </div>
    </div>
  </div>
{/if}

<!-- Issue Management Section -->
{#if !isLoading && !errorMessage}
  <div class="mb-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Issue Management</h1>

    </div>
    

    
    <div class="flex flex-col md:flex-row gap-4 mb-4">
      <!-- Search bar -->
      <div class="form-control flex-grow">
        <div class="input-group">
          <input type="text" placeholder="Search issues..." class="input input-bordered w-full" bind:value={searchQuery} />
          <button class="btn btn-square" aria-label="Search issues">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
          </button>
        </div>
      </div>
      
      <!-- Status filter -->
      <div class="form-control">
        <select class="select select-bordered" bind:value={statusFilter}>
          <option disabled selected>Filter by status</option>
          {#each statusOptions as status}
            <option value={status}>{status === 'all' ? 'All Statuses' : status.replace('_', ' ')}</option>
          {/each}
        </select>
      </div>
      
      <!-- Severity filter -->
      <div class="form-control">
        <select class="select select-bordered" bind:value={severityFilter}>
          <option disabled selected>Filter by severity</option>
          {#each severityOptions as severity}
            <option value={severity}>{severity === 'all' ? 'All Severities' : severity}</option>
          {/each}
        </select>
      </div>
      
      <!-- Create new issue button -->
      <button class="btn btn-primary">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
        New Issue
      </button>
    </div>
    
    <!-- Issues count -->
    <div class="text-sm text-gray-500 mb-2">
      Showing {filteredIssues.length} of {issues.length} issues
    </div>
  </div>
  
  <!-- Issues table -->
  <div class="overflow-x-auto">
    {#if isLoadingIssues}
      <div class="flex justify-center items-center py-8">
        <span class="loading loading-spinner loading-lg"></span>
        <span class="ml-2">Loading issues...</span>
      </div>
    {:else if issuesError}
      <div class="alert alert-error shadow-lg mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{issuesError}</span>
        <button class="btn btn-sm btn-ghost" on:click={loadIssues}>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Retry
        </button>
      </div>
    {/if}
    <table class="table table-zebra w-full" class:opacity-50={isLoadingIssues}>
      <thead>
        <tr>
          <th>ID</th>
          <th>Title</th>
          <th>Status</th>
          <th>Severity</th>
          <th>Reporter</th>
          <th>Created</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {#if filteredIssues.length === 0}
          <tr>
            <td colspan="7" class="text-center py-4">No issues found matching your filters.</td>
          </tr>
        {:else}
          {#each filteredIssues as issue}
            <tr class="hover">
              <td>#{issue.id}</td>
              <td>
                <div class="font-medium">{issue.title}</div>
                <div class="text-sm opacity-50 truncate max-w-xs">{issue.description}</div>
              </td>
              <td>
                <div class="dropdown dropdown-hover">
                  <button class="badge {getStatusBadgeClass(issue.status)} cursor-pointer border-0">
                    {isUpdating && activeIssue?.id === issue.id && activeIssue?.field === 'status' 
                      ? 'Updating...' 
                      : issue.status_display}
                  </button>
                  <ul class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
                    {#each statusOptions.filter(s => s !== 'all') as status}
                      {#if status !== issue.status}
                        <li>
                          <button 
                            on:click={() => handleUpdateIssue(issue.id, 'status', status)}
                            class="text-sm py-1"
                            disabled={isUpdating}
                          >
                            <span class="badge badge-sm {getStatusBadgeClass(status)} mr-2"></span>
                            {status === 'OPEN' ? 'Open' : 
                             status === 'TRIAGED' ? 'Triaged' : 
                             status === 'IN_PROGRESS' ? 'In Progress' : 
                             status === 'DONE' ? 'Done' : status}
                          </button>
                        </li>
                      {/if}
                    {/each}
                  </ul>
                </div>
              </td>
              <td>
                <div class="dropdown dropdown-hover">
                  <button class="badge {getSeverityBadgeClass(issue.severity)} cursor-pointer border-0">
                    {isUpdating && activeIssue?.id === issue.id && activeIssue?.field === 'severity' 
                      ? 'Updating...' 
                      : issue.severity_display}
                  </button>
                  <ul class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
                    {#each severityOptions.filter(s => s !== 'all') as severity}
                      {#if severity !== issue.severity}
                        <li>
                          <button 
                            on:click={() => handleUpdateIssue(issue.id, 'severity', severity)}
                            class="text-sm py-1"
                            disabled={isUpdating}
                          >
                            <span class="badge badge-sm {getSeverityBadgeClass(severity)} mr-2"></span>
                            {severity === 'LOW' ? 'Low' : 
                             severity === 'MEDIUM' ? 'Medium' : 
                             severity === 'HIGH' ? 'High' : 
                             severity === 'CRITICAL' ? 'Critical' : severity}
                          </button>
                        </li>
                      {/if}
                    {/each}
                  </ul>
                </div>
              </td>
              <td>
                {`${issue.created_by.first_name} ${issue.created_by.last_name}` || issue.created_by.email || 'Anonymous'}
              </td>
              <td>
                <div class="text-sm">{formatDate(issue.created_at)}</div>
              </td>
              <td>
                <div class="flex gap-2">
                  <button class="btn btn-sm btn-ghost btn-circle" aria-label="View issue details">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                  </button>
                  <button class="btn btn-sm btn-ghost btn-circle" aria-label="Edit issue">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                  </button>
                </div>
              </td>
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>
{/if}

<!-- Toast notification for successful updates -->
<div id="update-toast" class="toast toast-top toast-end hidden">
  <div class="alert alert-success">
    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
    <span>Issue updated successfully!</span>
  </div>
</div>

<!-- Error toast for update failures -->
{#if updateError}
<div class="toast toast-top toast-end">
  <div class="alert alert-error">
    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
    <span>{updateError}</span>
    <button class="btn btn-sm" on:click={() => updateError = ""}>Dismiss</button>
  </div>
</div>
{/if}
</div>