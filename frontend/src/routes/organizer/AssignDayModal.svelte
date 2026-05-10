<script>
    import { createEventDispatcher } from 'svelte';
    export let open = false;
    export let tasks = [];
    export let sections = [];
    export let schedule = [];

    const dispatch = createEventDispatcher();

    let search = '';
    let dragTaskId = null;
    let dragOverDate = null;

    const URGENCY = {
        upcoming:    { label: 'Upcoming',    bg: 'bg-slate-700',   text: 'text-slate-300'  },
        needs_doing: { label: 'Needs Doing', bg: 'bg-yellow-900',  text: 'text-yellow-300' },
        time_to_do:  { label: 'Time To Do',  bg: 'bg-orange-900',  text: 'text-orange-300' },
        overdue:     { label: 'Overdue',     bg: 'bg-red-900',     text: 'text-red-300'    },
    };

    $: days = schedule.slice(0, 7).map((d, i) => ({
        date: d.date,
        label: i === 0 ? 'Today' : d.day_name.slice(0, 3),
        dateLabel: d.date.slice(5),
        isWorkDay: d.is_work_day,
        taskCount: d.tasks.length,
    }));

    $: filtered = tasks
        .filter(t => t.schedule_type !== 'deep_work')
        .filter(t => !search.trim() || t.title.toLowerCase().includes(search.toLowerCase()));

    $: dragTask = tasks.find(t => t.id === dragTaskId) ?? null;

    function isPinned(date) {
        return dragTask?.pinned_dates?.includes(date) ?? false;
    }

    function sectionName(task) {
        return sections.find(s => s.id === task.section_id)?.name ?? '';
    }

    function onDragStart(e, taskId) {
        dragTaskId = taskId;
        e.dataTransfer.effectAllowed = 'move';
    }

    function onDragOver(e, date) {
        e.preventDefault();
        dragOverDate = date;
    }

    function onDragLeave() {
        dragOverDate = null;
    }

    function onDrop(e, date) {
        e.preventDefault();
        if (dragTaskId) dispatch('assign', { taskId: dragTaskId, date });
        dragTaskId = null;
        dragOverDate = null;
    }

    function onDragEnd() {
        dragTaskId = null;
        dragOverDate = null;
    }

    $: if (!open) { search = ''; dragTaskId = null; dragOverDate = null; }
</script>

{#if open}
    <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60" on:click|self={() => dispatch('close')}>
        <div class="bg-slate-900 border border-slate-700 rounded-xl shadow-2xl w-full max-w-2xl flex flex-col" style="max-height: 85vh;">

            <div class="flex items-center justify-between px-5 py-4 border-b border-slate-700 shrink-0">
                <div>
                    <h2 class="font-semibold text-slate-100">Assign Task to Day</h2>
                    <p class="text-xs text-slate-500 mt-0.5">Drag a task onto a day to add or remove it</p>
                </div>
                <button on:click={() => dispatch('close')} class="text-slate-400 hover:text-slate-200">
                    <svg xmlns="http://www.w3.org/2000/svg" class="size-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                </button>
            </div>

            <div class="px-4 pt-3 pb-2 shrink-0">
                <input
                    bind:value={search}
                    placeholder="Search tasks..."
                    class="w-full bg-slate-800 border border-slate-600 rounded px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500" />
            </div>

            <div class="flex-1 overflow-y-auto px-4 py-2 space-y-1 min-h-0">
                {#if filtered.length === 0}
                    <p class="text-sm text-slate-500 text-center py-6">No tasks found.</p>
                {:else}
                    {#each filtered as task}
                        {@const urgency = URGENCY[task.urgency] ?? URGENCY.upcoming}
                        {@const sec = sectionName(task)}
                        {@const pinnedCount = task.pinned_dates?.length ?? 0}
                        <div
                            draggable="true"
                            on:dragstart={(e) => onDragStart(e, task.id)}
                            on:dragend={onDragEnd}
                            class="flex items-center gap-2.5 px-3 py-2 rounded-lg border cursor-grab active:cursor-grabbing select-none transition-colors
                                {dragTaskId === task.id ? 'opacity-40 border-slate-600 bg-slate-800/30' : 'border-slate-700 bg-slate-800/50 hover:border-slate-600 hover:bg-slate-800'}">
                            <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5 shrink-0 text-slate-600" viewBox="0 0 24 24" fill="currentColor">
                                <circle cx="9" cy="6" r="1.5"/><circle cx="15" cy="6" r="1.5"/>
                                <circle cx="9" cy="12" r="1.5"/><circle cx="15" cy="12" r="1.5"/>
                                <circle cx="9" cy="18" r="1.5"/><circle cx="15" cy="18" r="1.5"/>
                            </svg>
                            <span class="px-1.5 py-0.5 text-xs rounded {urgency.bg} {urgency.text} whitespace-nowrap shrink-0">{urgency.label}</span>
                            <span class="text-sm text-slate-100 font-medium truncate flex-1">{task.title}</span>
                            {#if sec}<span class="text-xs text-slate-500 shrink-0 truncate max-w-[100px]">{sec}</span>{/if}
                            {#if pinnedCount > 0}
                                <span class="text-xs text-indigo-400 shrink-0">{pinnedCount} day{pinnedCount !== 1 ? 's' : ''}</span>
                            {/if}
                        </div>
                    {/each}
                {/if}
            </div>

            <div class="px-4 py-3 border-t border-slate-700 shrink-0">
                <p class="text-xs text-slate-500 mb-2">
                    {dragTask ? `Drop to ${isPinned(dragOverDate ?? '') ? 'remove from' : 'add to'} a day — highlighted days already assigned` : 'Drag a task above onto a day'}
                </p>
                <div class="grid grid-cols-7 gap-1.5">
                    {#each days as day}
                        {@const pinned = isPinned(day.date)}
                        {@const isOver = dragOverDate === day.date}
                        <div
                            on:dragover={(e) => onDragOver(e, day.date)}
                            on:dragleave={onDragLeave}
                            on:drop={(e) => onDrop(e, day.date)}
                            class="rounded-lg border-2 p-2 text-center transition-colors min-h-[72px] flex flex-col items-center justify-center gap-0.5
                                {isOver && pinned   ? 'border-rose-500 bg-rose-900/30'
                                : isOver            ? 'border-indigo-500 bg-indigo-900/30'
                                : pinned            ? 'border-indigo-600/60 bg-indigo-900/20'
                                : dragTaskId        ? 'border-slate-600 border-dashed bg-slate-800/30'
                                                    : 'border-slate-700 bg-slate-800/40'}
                                {!day.isWorkDay ? 'opacity-50' : ''}">
                            <div class="text-xs font-semibold {isOver ? (pinned ? 'text-rose-300' : 'text-indigo-300') : pinned ? 'text-indigo-400' : 'text-slate-300'}">{day.label}</div>
                            <div class="text-xs text-slate-500">{day.dateLabel}</div>
                            {#if pinned}
                                <div class="text-xs {isOver ? 'text-rose-400' : 'text-indigo-400'}">
                                    {isOver ? '✕ remove' : '✓ assigned'}
                                </div>
                            {:else if isOver}
                                <div class="text-xs text-indigo-400">+ add</div>
                            {:else if day.taskCount > 0}
                                <div class="text-xs text-slate-600">{day.taskCount} task{day.taskCount !== 1 ? 's' : ''}</div>
                            {:else if day.isWorkDay}
                                <div class="text-xs text-slate-700 italic">Free</div>
                            {:else}
                                <div class="text-xs text-slate-700 italic">Off</div>
                            {/if}
                        </div>
                    {/each}
                </div>
            </div>

        </div>
    </div>
{/if}
