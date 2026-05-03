<script>
    import { createEventDispatcher, onDestroy } from 'svelte';
    export let session;
    export let task;

    const dispatch = createEventDispatcher();
    let elapsed = '';
    let interval;

    function tick() {
        const start = new Date(session.start_time + 'Z');
        const diff = Math.floor((Date.now() - start.getTime()) / 1000);
        const h = Math.floor(diff / 3600).toString().padStart(2, '0');
        const m = Math.floor((diff % 3600) / 60).toString().padStart(2, '0');
        const s = (diff % 60).toString().padStart(2, '0');
        elapsed = `${h}:${m}:${s}`;
    }

    $: if (session) {
        clearInterval(interval);
        tick();
        interval = setInterval(tick, 1000);
    }

    onDestroy(() => clearInterval(interval));
</script>

<div class="flex items-center gap-3 px-4 py-2 bg-emerald-900/40 border border-emerald-700/50 rounded-lg">
    <span class="relative flex h-2.5 w-2.5">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
        <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
    </span>
    <span class="text-emerald-300 font-medium text-sm">{task?.title ?? 'Task'}</span>
    <span class="font-mono text-emerald-200 text-sm">{elapsed}</span>
    <div class="ml-auto flex gap-2">
        <button
            on:click={() => dispatch('stop')}
            class="px-3 py-1 text-xs font-semibold bg-emerald-700 hover:bg-emerald-600 text-white rounded transition-colors">
            Stop
        </button>
        <button
            on:click={() => dispatch('complete')}
            class="px-3 py-1 text-xs font-semibold bg-slate-600 hover:bg-slate-500 text-white rounded transition-colors">
            Mark Done
        </button>
    </div>
</div>
