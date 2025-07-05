<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import Chart from 'chart.js/auto';
  import type { ChartData, ChartOptions, ChartType } from 'chart.js';
  
  export let type: ChartType = 'bar';
  export let data: ChartData;
  export let options: ChartOptions = {};
  export let title = '';
  
  let chartElement: HTMLCanvasElement;
  let chartInstance: Chart;
  
  onMount(() => {
    if (chartElement) {
      chartInstance = new Chart(chartElement, {
        type,
        data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          ...options
        }
      });
    }
  });
  
  onDestroy(() => {
    if (chartInstance) {
      chartInstance.destroy();
    }
  });
  
  // Update chart when data changes
  $: if (chartInstance && data) {
    chartInstance.data = data;
    chartInstance.update();
  }
</script>

<div class="chart-container">
  {#if title}
    <h3 class="text-xl font-bold mb-2">{title}</h3>
  {/if}
  <div class="chart-wrapper">
    <canvas bind:this={chartElement}></canvas>
  </div>
</div>

<style>
  .chart-container {
    width: 100%;
    margin-bottom: 1rem;
  }
  
  .chart-wrapper {
    position: relative;
    height: 300px;
    width: 100%;
  }
</style>