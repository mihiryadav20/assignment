<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { BaseUrl, ApiEndpoints } from '$lib/url';
  import Chart from './Chart.svelte';
  
  interface StatsResponse {
    status_counts: Record<string, number>;
    severity_counts: Record<string, number>;
    total_issues: number;
  }

  let isLoading = true;
  let error = '';
  let statusData: Record<string, number> = {};
  let severityData: Record<string, number> = {};
  let totalIssues = 0;
  
  // Status and severity labels
  const statusLabels = ['OPEN', 'TRIAGED', 'IN_PROGRESS', 'DONE'];
  const severityLabels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'];
  
  // Chart colors
  const statusColors = ['#2563eb', '#0ea5e9', '#f59e42', '#22c55e'];
  const severityColors = ['#38bdf8', '#fbbf24', '#ef4444', '#7c3aed'];
  
  onMount(async () => {
    const token = localStorage.getItem('auth_token');
    
    if (!token) {
      goto('/login');
      return;
    }
    
    await fetchStats(token);
  });
  
  async function fetchStats(token: string) {
    isLoading = true;
    error = '';
    
    try {
      const response = await fetch(`${BaseUrl}/api/issues/stats/`, {
        method: 'GET',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      });
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      statusData = data.status_counts;
      severityData = data.severity_counts;
      totalIssues = data.total_issues;
    } catch (e) {
      console.error('Error fetching stats:', e);
      error = e instanceof Error ? e.message : 'Failed to fetch issue statistics';
    } finally {
      isLoading = false;
    }
  }
  
  // Prepare chart data
  $: statusChartData = {
    labels: statusLabels,
    datasets: [{
      label: 'Issue Status',
      data: statusLabels.map(label => statusData[label] || 0),
      backgroundColor: statusColors,
      borderColor: statusColors.map(color => color + '99'),
      borderWidth: 1
    }]
  };
  
  $: severityChartData = {
    labels: severityLabels,
    datasets: [{
      label: 'Issue Severity',
      data: severityLabels.map(label => severityData[label] || 0),
      backgroundColor: severityColors,
      borderColor: severityColors.map(color => color + '99'),
      borderWidth: 1
    }]
  };
  
  const chartOptions = {
    plugins: {
      legend: {
        display: true,
        position: 'bottom' as const
      },
      tooltip: {
        callbacks: {
          label: function(context: any) {
            return `Count: ${context.raw}`;
          }
        }
      }
    }
  };
</script>

<div class="min-h-screen bg-base-200 p-4">
  <div class="navbar bg-base-100 rounded-lg shadow-md mb-6">
    <div class="flex-1">
      <h1 class="text-xl font-bold">Issue Statistics</h1>
    </div>
    <div class="flex-none">
      <button class="btn btn-primary" on:click={() => goto('/maintainer')}>Back to Dashboard</button>
    </div>
  </div>
  
  {#if isLoading}
    <div class="flex justify-center items-center h-64">
      <div class="loading loading-spinner loading-lg"></div>
    </div>
  {:else if error}
    <div class="alert alert-error shadow-lg">
      <div>
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        <span>{error}</span>
      </div>
    </div>
  {:else}
    <!-- Total Issues at the top -->
    <div class="mb-6 bg-base-100 p-6 rounded-lg shadow-md">
      <h2 class="text-lg font-semibold mb-2">Total Issues</h2>
      <p class="text-3xl font-bold">{totalIssues}</p>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Status Chart -->
      <div class="bg-base-100 p-6 rounded-lg shadow-md">
        <h2 class="text-lg font-semibold mb-4">Issue Status Distribution</h2>
        <!-- Counts above chart -->
        <div class="mb-2 grid grid-cols-2 gap-2">
          {#each statusLabels as label, i}
            <div class="flex items-center">
              <div class="w-3 h-3 rounded-full mr-2" style="background-color: {statusColors[i]}"></div>
              <span class="text-sm">{label}: {statusData[label] || 0}</span>
            </div>
          {/each}
        </div>
        <div class="h-64">
          <Chart data={statusChartData} options={chartOptions} type="bar" />
        </div>
      </div>
      
      <!-- Severity Chart -->
      <div class="bg-base-100 p-6 rounded-lg shadow-md">
        <h2 class="text-lg font-semibold mb-4">Issue Severity Distribution</h2>
        <!-- Counts above chart -->
        <div class="mb-2 grid grid-cols-2 gap-2">
          {#each severityLabels as label, i}
            <div class="flex items-center">
              <div class="w-3 h-3 rounded-full mr-2" style="background-color: {severityColors[i]}"></div>
              <span class="text-sm">{label}: {severityData[label] || 0}</span>
            </div>
          {/each}
        </div>
        <div class="h-64">
          <Chart data={severityChartData} options={chartOptions} type="bar" />
        </div>
      </div>
    </div>
  {/if}
</div>