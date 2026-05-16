<script>
    import { createEventDispatcher } from 'svelte';
    export let task;
    const dispatch = createEventDispatcher();
</script>

<div class="flex items-center gap-3 px-4 py-2 bg-violet-900/40 border border-violet-700/50 rounded-lg">
    <span class="relative flex h-2.5 w-2.5 shrink-0">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-violet-400 opacity-75"></span>
        <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-violet-500"></span>
    </span>
    <span class="text-violet-300 font-medium text-sm truncate min-w-0">{task.title}</span>
    <span class="text-xs text-violet-500 shrink-0">{task.pulse_duration_min}m</span>
    <div class="ml-auto shrink-0">
        <button
            on:click={() => dispatch('dismiss')}
            class="px-3 py-1 text-xs font-semibold bg-violet-700 hover:bg-violet-600 text-white rounded transition-colors">
            Dismiss
        </button>
    </div>
</div>
