<script>
    import { createEventDispatcher } from 'svelte';
    export let task;
    export let activeSessionTaskId = null;
    export let sections = [];
    export let compact = false;
    export let skippable = false;
    export let completingId = null;
    export let todayMin = 0;

    const dispatch = createEventDispatcher();

    const URGENCY = {
        upcoming:    { label: 'Upcoming',     bg: 'bg-slate-700',   text: 'text-slate-300'  },
        needs_doing: { label: 'Needs Doing',  bg: 'bg-yellow-900',  text: 'text-yellow-300' },
        time_to_do:  { label: 'Time To Do',   bg: 'bg-orange-900',  text: 'text-orange-300' },
        overdue:     { label: 'Overdue',      bg: 'bg-red-900',     text: 'text-red-300'    },
    };

    const PRIORITY_STYLE = {
        high: { label: '↑ High', cls: 'text-rose-400' },
        low:  { label: '↓ Low',  cls: 'text-slate-500' },
    };

    const PRESETS = [1, 5, 15, 30, 60];

    const DAY_ABBR = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];

    $: isCompleting = completingId === task.id;
    $: urgency = URGENCY[task.urgency] ?? URGENCY.upcoming;
    $: isActive = activeSessionTaskId === task.id;
    $: sectionName = sections.find(s => s.id === task.section_id)?.name ?? '';
    $: daysSince = task.days_since != null ? `${task.days_since}d ago` : 'Never done';
    $: priorityStyle = PRIORITY_STYLE[task.priority] ?? null;
    $: isDeepWork = task.schedule_type === 'deep_work';
    $: isPulse = task.schedule_type === 'pulse';
    $: scheduledDaysLabel = isDeepWork && task.scheduled_days?.length
        ? task.scheduled_days.map(d => DAY_ABBR[d]).join(' ')
        : '';
    $: if (isActive) startOpen = false;

    let startOpen = false;
    let customMin = localStorage.getItem('timerCustomMin') ?? '';

    function fmtDuration(min) {
        if (min < 60) return `${Math.round(min)}m`;
        const h = Math.floor(min / 60);
        const m = Math.round(min % 60);
        return m > 0 ? `${h}h ${m}m` : `${h}h`;
    }

    function fmtRange(min, max) {
        return min === max ? `${min}m` : `${min}–${max}m`;
    }

    function pick(timerMin) {
        startOpen = false;
        dispatch('start', { task, timerMin });
    }

    function pickCustom() {
        const m = parseFloat(customMin);
        if (m > 0) {
            localStorage.setItem('timerCustomMin', customMin);
            pick(m);
        }
    }
</script>

<div class="rounded-lg border {isActive ? 'border-emerald-600 bg-emerald-900/20' : isPulse ? 'border-violet-600/70 bg-violet-900/10 pulse-border' : 'border-slate-700 bg-slate-800/50'} {compact ? 'p-2 space-y-1' : 'p-3 space-y-2'} transition-colors">
    <div class="flex items-start gap-2">
        <span class="mt-0.5 px-1.5 py-0.5 text-xs rounded {urgency.bg} {urgency.text} whitespace-nowrap shrink-0">{urgency.label}</span>
        <span class="{compact ? 'text-sm' : ''} font-medium text-slate-100 leading-snug">{task.title}</span>
        <div class="ml-auto flex items-center gap-1 shrink-0">
            <button title="Edit" on:click={() => dispatch('edit', task)} class="p-1 text-slate-400 hover:text-slate-200 rounded transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
            </button>
            <button title="Delete" on:click={() => dispatch('delete', task)} class="p-1 text-slate-400 hover:text-red-400 rounded transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/>
                </svg>
            </button>
        </div>
    </div>

    {#if task.description && !compact}
        <p class="text-xs text-slate-400 leading-relaxed">{task.description}</p>
    {/if}

    {#if task.pinned_dates?.length > 0}
        <div class="text-xs text-indigo-400 font-medium">
            Scheduled: {task.pinned_dates.slice().sort().join(', ')}
        </div>
    {/if}

    <div class="flex flex-wrap gap-x-3 gap-y-0.5 text-xs text-slate-500">
        {#if isPulse}
            <span class="text-violet-400">◉ Pulse</span>
        {:else if isDeepWork}
            <span class="text-emerald-400">◎ Fixed</span>
        {/if}
        <span title="Duration">
            {#if isPulse}
                {task.pulse_duration_min}m · every {task.pulse_interval_min}m
            {:else if isDeepWork && task.daily_target_min}
                {task.daily_target_min}m/day
            {:else}
                {fmtRange(task.min_duration_min, task.max_duration_min)}
            {/if}
        </span>
        {#if !compact && isDeepWork && scheduledDaysLabel}
            <span title="Scheduled days" class="text-emerald-600">{scheduledDaysLabel}</span>
        {:else if !compact && !isDeepWork && !isPulse}
            <span title="Recurrence">every {task.recurrence_min_days}–{task.recurrence_max_days}d</span>
        {/if}
        {#if !isDeepWork && !isPulse}<span title="Last done">{daysSince}</span>{/if}
        {#if !compact && sectionName}<span class="text-slate-400">{sectionName}</span>{/if}
        {#if priorityStyle}<span class={priorityStyle.cls}>{priorityStyle.label}</span>{/if}
        {#if task.overtime_eligible}<span class="text-amber-500">OT</span>{/if}
        {#if todayMin > 0}<span class="text-emerald-400">{fmtDuration(todayMin)} today</span>{/if}
    </div>

    <div class="flex gap-2">
        <div class="relative flex-1">
            {#if isActive}
                <button
                    on:click={() => dispatch('stop', task)}
                    class="w-full {compact ? 'py-1' : 'py-1.5'} text-xs font-semibold bg-emerald-700 hover:bg-emerald-600 text-white rounded transition-colors">
                    Stop
                </button>
            {:else}
                <button
                    on:click={() => startOpen = !startOpen}
                    class="w-full {compact ? 'py-1' : 'py-1.5'} text-xs font-semibold bg-indigo-700 hover:bg-indigo-600 text-white rounded transition-colors">
                    Start
                </button>
            {/if}

            {#if startOpen}
                <div class="fixed inset-0 z-40" on:click={() => startOpen = false}></div>
                <div class="absolute bottom-full left-0 mb-1 z-50 bg-slate-900 border border-slate-700 rounded-lg p-2.5 shadow-2xl w-60">
                    <div class="flex gap-1 mb-2">
                        {#each PRESETS as min}
                            <button on:click={() => pick(min)} class="flex-1 py-1.5 text-xs font-semibold bg-slate-700 hover:bg-indigo-600 text-slate-200 rounded transition-colors">
                                {min}m
                            </button>
                        {/each}
                    </div>
                    <div class="flex gap-1 mb-2">
                        <input
                            type="number"
                            bind:value={customMin}
                            min="0.1"
                            step="any"
                            placeholder="min"
                            on:keydown={(e) => e.key === 'Enter' && pickCustom()}
                            class="w-16 shrink-0 bg-slate-800 border border-slate-600 rounded px-2 py-1 text-xs text-slate-100 focus:outline-none focus:border-indigo-500" />
                        <button
                            on:click={pickCustom}
                            disabled={!customMin}
                            class="flex-1 py-1 text-xs font-semibold bg-slate-700 hover:bg-indigo-600 disabled:opacity-40 text-slate-200 rounded transition-colors">
                            Custom Time
                        </button>
                    </div>
                    <button on:click={() => pick(null)} class="w-full py-1.5 text-xs font-semibold bg-indigo-700 hover:bg-indigo-600 text-white rounded transition-colors">
                        Stopwatch
                    </button>
                </div>
            {/if}
        </div>

        <button
            on:click={() => dispatch('complete', task)}
            disabled={isCompleting}
            class="px-3 {compact ? 'py-1' : 'py-1.5'} text-xs font-semibold bg-slate-700 hover:bg-slate-600 disabled:opacity-40 disabled:cursor-not-allowed text-slate-200 rounded transition-colors whitespace-nowrap">
            {#if isCompleting}
                <span class="flex gap-1 items-center justify-center">
                    <span class="w-1 h-1 rounded-full bg-slate-300 animate-bounce [animation-delay:-0.3s]"></span>
                    <span class="w-1 h-1 rounded-full bg-slate-300 animate-bounce [animation-delay:-0.15s]"></span>
                    <span class="w-1 h-1 rounded-full bg-slate-300 animate-bounce"></span>
                </span>
            {:else}
                Mark Done
            {/if}
        </button>

        {#if skippable && !isActive}
            <button
                on:click={() => dispatch('skip', task)}
                class="px-2 {compact ? 'py-1' : 'py-1.5'} text-xs text-slate-600 hover:text-slate-400 transition-colors whitespace-nowrap">
                Not today
            </button>
        {/if}
    </div>
</div>

<style>
    @keyframes pulse-border {
        0%, 100% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0); }
        50%       { box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.25); }
    }
    :global(.pulse-border) {
        animation: pulse-border 2s ease-in-out infinite;
    }
</style>
