<script>
    import { createEventDispatcher } from 'svelte';
    export let task;
    export let remainingSec = null;

    const dispatch = createEventDispatcher();

    function fmtCountdown(sec) {
        const m = Math.floor(sec / 60);
        const s = sec % 60;
        return `${m}:${String(s).padStart(2, '0')}`;
    }

    $: timing = remainingSec !== null;
</script>

<div class="flex items-center gap-3 px-4 py-2 bg-violet-900/40 border border-violet-700/50 rounded-lg">
    <span class="relative flex h-2.5 w-2.5 shrink-0">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-violet-400 opacity-75"></span>
        <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-violet-500"></span>
    </span>
    <span class="text-violet-300 font-medium text-sm truncate min-w-0">{task.title}</span>
    {#if timing}
        <span class="text-sm font-mono font-semibold text-violet-200 shrink-0">{fmtCountdown(remainingSec)}</span>
    {:else}
        <span class="text-xs text-violet-500 shrink-0">{task.pulse_duration_min}m</span>
    {/if}
    <div class="ml-auto flex items-center gap-2 shrink-0">
        {#if timing}
            <button
                on:click={() => dispatch('done')}
                class="px-3 py-1 text-xs font-semibold bg-emerald-700 hover:bg-emerald-600 text-white rounded transition-colors">
                Done
            </button>
        {:else}
            <button
                on:click={() => dispatch('start')}
                class="px-3 py-1 text-xs font-semibold bg-indigo-700 hover:bg-indigo-600 text-white rounded transition-colors">
                Start
            </button>
            <button
                on:click={() => dispatch('dismiss')}
                class="px-3 py-1 text-xs font-semibold bg-violet-800/60 hover:bg-violet-700/60 text-violet-300 rounded transition-colors">
                Dismiss
            </button>
        {/if}
    </div>
</div>
