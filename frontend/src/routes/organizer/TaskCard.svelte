<script>
    import { createEventDispatcher } from 'svelte';
    export let task;
    export let activeSessionTaskId = null;
    export let sections = [];
    export let compact = false;
    export let skippable = false;

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

    $: urgency = URGENCY[task.urgency] ?? URGENCY.upcoming;
    $: isActive = activeSessionTaskId === task.id;
    $: sectionName = sections.find(s => s.id === task.section_id)?.name ?? '';
    $: daysSince = task.days_since != null ? `${task.days_since}d ago` : 'Never done';
    $: priorityStyle = PRIORITY_STYLE[task.priority] ?? null;

    function fmtRange(min, max) {
        return min === max ? `${min}m` : `${min}–${max}m`;
    }
</script>

<div class="rounded-lg border {isActive ? 'border-emerald-600 bg-emerald-900/20' : 'border-slate-700 bg-slate-800/50'} {compact ? 'p-2 space-y-1' : 'p-3 space-y-2'} transition-colors">
    <div class="flex items-start gap-2">
        <span class="mt-0.5 px-1.5 py-0.5 text-xs rounded {urgency.bg} {urgency.text} whitespace-nowrap shrink-0">{urgency.label}</span>
        <span class="{compact ? 'text-sm' : ''} font-medium text-slate-100 leading-snug">{task.title}</span>
        <div class="ml-auto flex items-center gap-1 shrink-0">
            <button
                title="Edit"
                on:click={() => dispatch('edit', task)}
                class="p-1 text-slate-400 hover:text-slate-200 rounded transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
            </button>
            <button
                title="Delete"
                on:click={() => dispatch('delete', task)}
                class="p-1 text-slate-400 hover:text-red-400 rounded transition-colors">
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
        <span title="Task type">
            {#if task.task_type === 'deep'}
                <span class="text-indigo-400">● Deep</span>
            {:else}
                <span class="text-cyan-400">● Filler</span>
            {/if}
        </span>
        <span title="Duration">{fmtRange(task.min_duration_min, task.max_duration_min)}</span>
        {#if !compact}<span title="Recurrence">every {task.recurrence_min_days}–{task.recurrence_max_days}d</span>{/if}
        <span title="Last done">{daysSince}</span>
        {#if !compact && sectionName}<span class="text-slate-400">{sectionName}</span>{/if}
        {#if priorityStyle}<span class={priorityStyle.cls}>{priorityStyle.label}</span>{/if}
        {#if task.overtime_eligible}<span class="text-amber-500">OT</span>{/if}
    </div>

    <div class="flex gap-2">
        {#if isActive}
            <button
                on:click={() => dispatch('stop', task)}
                class="flex-1 {compact ? 'py-1' : 'py-1.5'} text-xs font-semibold bg-emerald-700 hover:bg-emerald-600 text-white rounded transition-colors">
                Stop
            </button>
        {:else}
            <button
                on:click={() => dispatch('start', task)}
                disabled={!!activeSessionTaskId}
                class="flex-1 {compact ? 'py-1' : 'py-1.5'} text-xs font-semibold bg-indigo-700 hover:bg-indigo-600 disabled:opacity-40 disabled:cursor-not-allowed text-white rounded transition-colors">
                Start
            </button>
        {/if}
        <button
            on:click={() => dispatch('complete', task)}
            disabled={!isActive && !!activeSessionTaskId}
            class="px-3 {compact ? 'py-1' : 'py-1.5'} text-xs font-semibold bg-slate-700 hover:bg-slate-600 disabled:opacity-40 disabled:cursor-not-allowed text-slate-200 rounded transition-colors whitespace-nowrap">
            Mark Done
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
