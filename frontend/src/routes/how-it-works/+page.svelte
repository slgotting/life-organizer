<script>
    const SECTIONS = [
        {
            title: 'Task Types',
            entries: [
                {
                    label: 'Recurring',
                    body: `The default task type. You set a recurrence window (e.g. every 2–5 days) and the scheduler automatically decides which day to place it based on urgency and available time. Urgency escalates the longer it has been since you last completed it — sliding from Upcoming → Needs Doing → Time To Do → Overdue as the window closes. Use this for anything with a natural cadence: workouts, chores, habits.`,
                },
                {
                    label: 'Fixed',
                    body: `Tasks committed to specific days of the week (e.g. Mon, Wed, Fri). You set a daily target in minutes; the scheduler places the task on those days and tracks your pace across the week using completed session time. Urgency is pace-based: if you are behind your weekly average the task shows as more urgent, ahead means Upcoming. Use this for ongoing commitments with a weekly structure — instrument practice, a side project, language study.`,
                },
                {
                    label: 'One-off',
                    body: `A task that only needs to be done once. It behaves like a Recurring task for scheduling purposes but disappears from the active list once marked done. Use this for discrete errands or project milestones.`,
                },
            ],
        },
        {
            title: 'Urgency Colors',
            entries: [
                { label: 'Upcoming', color: 'bg-slate-700 text-slate-300', body: 'Not yet due. The task is within its comfortable recurrence window or ahead of its weekly pace target.' },
                { label: 'Needs Doing', color: 'bg-yellow-900 text-yellow-300', body: 'Getting close. The task is past the first third of its recurrence window.' },
                { label: 'Time To Do', color: 'bg-orange-900 text-orange-300', body: 'Should be done soon. Past the two-thirds mark of its window.' },
                { label: 'Overdue', color: 'bg-red-900 text-red-300', body: 'Past its maximum recurrence window or significantly behind its weekly pace target.' },
            ],
        },
        {
            title: 'Sections',
            entries: [
                {
                    label: 'What they are',
                    body: `Sections represent areas of your life or categories of work (e.g. Health, Deep Work, Admin). Each task belongs to a section. The scheduler only places a task into its section\'s time window, so tasks never bleed across unrelated blocks.`,
                },
                {
                    label: 'Configuring time blocks',
                    body: `In the sidebar, each section can be assigned a schedule per day of the week — either a time block (start hour to end hour) or a fixed duration. The scheduler uses remaining time in those blocks as the pool from which tasks are scheduled. Today\'s pool accounts for time already elapsed.`,
                },
            ],
        },
        {
            title: 'Scheduling',
            entries: [
                {
                    label: 'How tasks are placed',
                    body: `The scheduler runs a day-first greedy algorithm across the next 7 days. Fixed tasks are placed first on their specified weekdays, then pinned tasks (specific dates you assigned), then Recurring and One-off tasks in urgency/priority order. Each task consumes its average duration ((min + max) / 2) from its section\'s pool, so the schedule fits more tasks without being over-optimistic.`,
                },
                {
                    label: 'Priority',
                    body: `Within the same urgency level, High priority tasks are placed before Medium, and Medium before Low.`,
                },
                {
                    label: 'Overload warning',
                    body: `A red banner appears when urgent tasks cannot fit into available time this week, or when a Fixed task is missing from its scheduled day due to insufficient capacity.`,
                },
                {
                    label: 'Capacity warning',
                    body: `An amber banner appears when total weekly task demand is at or above 85% of total configured weekly capacity — a signal to consider reducing your task load before things overflow.`,
                },
            ],
        },
        {
            title: 'Views',
            entries: [
                {
                    label: 'Today',
                    body: `Shows tasks scheduled for today, grouped by section. Each card shows urgency, duration estimate, recurrence or scheduled days, and time already logged today. You can start a timer, mark done, or skip (push to tomorrow) from here.`,
                },
                {
                    label: 'This Week',
                    body: `A 7-column grid showing tasks across the next 7 days. Drag a task chip from one day to another to manually pin it to a new date — a "Recompute Schedule" button appears after drops so you can trigger a full re-evaluation when ready. Click any task chip to edit it. A legend at the top shows urgency colors and the green ring used for Fixed tasks.`,
                },
                {
                    label: 'All Tasks / Fixed / Recurring / One-off',
                    body: `Task management tabs. All four tabs share the section sidebar on the left — click a section to filter, or click "All" to see everything. Use these tabs to create, edit, and delete tasks.`,
                },
                {
                    label: 'History',
                    body: `A time-grid calendar showing completed work sessions for the selected week. Click a session block to edit its start/end times or delete it. Click any empty area on a day column to manually log a past session — pick the task, adjust the times, and save.`,
                },
                {
                    label: 'Stats',
                    body: `Cumulative and this-week time breakdowns by section and by individual task.`,
                },
            ],
        },
        {
            title: 'Sessions & Timer',
            entries: [
                {
                    label: 'Starting a session',
                    body: `Press Start on any task card. You can choose a preset duration (1m, 5m, 15m, 30m, 60m), enter a custom time, or use the Stopwatch mode (no countdown). If another session is already running, you will be asked to confirm stopping it first.`,
                },
                {
                    label: 'Timer bar',
                    body: `The active timer appears at the top of every page. It shows the task name, elapsed or remaining time, and turns amber with an audio beep when the countdown ends. Use Silence to stop the beeping, Stop to save the session, or Mark Done to save and complete the task simultaneously.`,
                },
                {
                    label: 'Keep-awake',
                    body: `While a session is running the app requests a screen wake lock (web) or native keep-awake (iOS/Android) so the timer is not interrupted by device sleep. The lock is released automatically when the session ends.`,
                },
                {
                    label: 'Logging past sessions',
                    body: `Go to History, click an empty slot on any day, choose a task, set start and end times, and press Log Session. The schedule urgency for Fixed tasks updates automatically after logging.`,
                },
            ],
        },
        {
            title: 'Assign to Day',
            entries: [
                {
                    label: 'Pinning a task to a specific date',
                    body: `Open the "Assign to Day" modal (available from Today and This Week). Drag any Recurring or One-off task onto a day to pin it — highlighted days are already assigned. Dragging again removes the pin. Fixed tasks are excluded since their schedule is defined by day-of-week, not individual dates.`,
                },
            ],
        },
    ];
</script>

<div class="max-w-3xl mx-auto px-4 py-8 space-y-10">
    <div>
        <h1 class="text-2xl font-bold text-slate-100 mb-1">How It Works</h1>
        <p class="text-slate-400 text-sm">A living reference for the scheduler. Updated as features change.</p>
    </div>

    {#each SECTIONS as section}
        <div>
            <h2 class="text-base font-semibold text-indigo-400 mb-3 pb-1 border-b border-slate-700">{section.title}</h2>
            <div class="space-y-3">
                {#each section.entries as entry}
                    <div class="grid gap-x-4 items-baseline" style="grid-template-columns: 11rem 1fr;">
                        <div class="text-right">
                            {#if entry.color}
                                <span class="inline-block px-2 py-0.5 text-xs rounded font-medium {entry.color} whitespace-nowrap">{entry.label}</span>
                            {:else}
                                <span class="text-xs font-semibold text-slate-300 whitespace-nowrap">{entry.label}</span>
                            {/if}
                        </div>
                        <p class="text-sm text-slate-400 leading-relaxed">{entry.body}</p>
                    </div>
                {/each}
            </div>
        </div>
    {/each}
</div>
