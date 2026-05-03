<script>
    export let stats;    // { sections: [{id,name,total_min}], tasks: [{id,title,section_id,section_name,week_min,total_min}] }
    export let sections; // [{id,name}] for palette ordering

    const COLORS = ['#6366f1', '#7c3aed', '#06b6d4', '#14b8a6', '#f59e0b', '#f43f5e'];

    function colorFor(sid) {
        const idx = sections.findIndex(s => s.id === sid);
        return COLORS[Math.max(0, idx) % COLORS.length];
    }

    const R = 35, CX = 50, CY = 50;
    const CIRC = 2 * Math.PI * R;

    $: totalMin  = stats.sections.reduce((s, x) => s + x.total_min, 0);
    $: weekMin   = stats.tasks.reduce((s, t) => s + t.week_min, 0);
    $: taskCount = stats.tasks.length;

    $: pieSegments = (() => {
        let off = 0;
        return stats.sections
            .filter(s => s.total_min > 0)
            .map(s => {
                const len = (s.total_min / totalMin) * CIRC;
                const seg = { ...s, color: colorFor(s.id), len, off };
                off += len;
                return seg;
            });
    })();

    $: tabs = [{ id: 'all', name: 'All' }, ...stats.sections.filter(s => s.total_min > 0)];

    let activeTab = 'all';
    let sortCol = 'total_min';
    let sortDir = 'desc';

    function toggleSort(col) {
        if (sortCol === col) sortDir = sortDir === 'desc' ? 'asc' : 'desc';
        else { sortCol = col; sortDir = 'desc'; }
    }

    $: filtered = activeTab === 'all'
        ? stats.tasks
        : stats.tasks.filter(t => t.section_id === activeTab);

    $: sorted = [...filtered].sort((a, b) => {
        const m = sortDir === 'desc' ? -1 : 1;
        return sortCol === 'title'
            ? m * a.title.localeCompare(b.title)
            : m * ((a[sortCol] ?? 0) - (b[sortCol] ?? 0));
    });

    function fmt(min) {
        if (!min) return '—';
        const h = Math.floor(min / 60), m = min % 60;
        return h ? (m ? `${h}h ${m}m` : `${h}h`) : `${m}m`;
    }

    const SUMMARY = [
        { label: 'Last 7 Days', key: 'weekMin',   format: fmt },
        { label: 'All Time',    key: 'totalMin',   format: fmt },
        { label: 'Tasks',       key: 'taskCount',  format: v => v },
        { label: 'Sections',    key: 'pieCount',   format: v => v },
    ];

    const COLS = [
        { id: 'title',     label: 'Task',        right: false },
        { id: 'week_min',  label: 'Last 7 Days', right: true  },
        { id: 'total_min', label: 'All Time',    right: true  },
    ];
</script>

<div class="space-y-4">
    <!-- Top: pie chart + summary cards -->
    <div class="grid sm:grid-cols-2 gap-4">

        <!-- Donut chart -->
        <div class="bg-slate-800/50 border border-slate-700 rounded-xl p-5">
            {#if totalMin === 0}
                <div class="flex items-center justify-center h-36 text-slate-500 text-sm">No sessions recorded yet.</div>
            {:else}
                <div class="flex items-center gap-6">
                    <svg viewBox="0 0 100 100" class="w-36 h-36 shrink-0" aria-hidden="true">
                        <circle cx={CX} cy={CY} r={R} fill="none" stroke="#1e293b" stroke-width="20" />
                        {#each pieSegments as seg}
                            <circle
                                cx={CX} cy={CY} r={R}
                                fill="none"
                                stroke={seg.color}
                                stroke-width="20"
                                stroke-linecap="butt"
                                stroke-dasharray="{seg.len} {CIRC}"
                                stroke-dashoffset={-seg.off}
                                transform="rotate(-90 {CX} {CY})" />
                        {/each}
                        <text x={CX} y={CY - 5} text-anchor="middle" fill="#f1f5f9" font-size="10" font-weight="600" font-family="sans-serif">
                            {fmt(totalMin)}
                        </text>
                        <text x={CX} y={CY + 7} text-anchor="middle" fill="#475569" font-size="7" font-family="sans-serif">
                            all time
                        </text>
                    </svg>

                    <!-- Legend -->
                    <div class="flex-1 space-y-2 min-w-0">
                        {#each pieSegments as seg}
                            <div class="flex items-center gap-2 min-w-0">
                                <div class="w-2.5 h-2.5 rounded-sm shrink-0" style="background:{seg.color}"></div>
                                <span class="text-xs text-slate-300 truncate flex-1">{seg.name}</span>
                                <span class="text-xs text-slate-500 shrink-0">{fmt(seg.total_min)}</span>
                            </div>
                        {/each}
                    </div>
                </div>
            {/if}
        </div>

        <!-- Summary cards -->
        <div class="grid grid-cols-2 gap-3">
            {#each [['Last 7 Days', fmt(weekMin)], ['All Time', fmt(totalMin)], ['Tasks Tracked', taskCount], ['Sections Active', pieSegments.length]] as [label, value]}
                <div class="bg-slate-800/50 border border-slate-700 rounded-xl p-4 flex flex-col justify-between">
                    <div class="text-xs text-slate-500">{label}</div>
                    <div class="text-2xl font-bold text-slate-100 mt-2">{value}</div>
                </div>
            {/each}
        </div>
    </div>

    <!-- Task table -->
    <div class="bg-slate-800/50 border border-slate-700 rounded-xl overflow-hidden">

        <!-- Section tabs -->
        <div class="flex border-b border-slate-700 overflow-x-auto">
            {#each tabs as t}
                <button
                    on:click={() => activeTab = t.id}
                    class="flex items-center gap-1.5 px-4 py-2.5 text-sm font-medium whitespace-nowrap transition-colors
                        {activeTab === t.id ? 'text-indigo-400 border-b-2 border-indigo-500 -mb-px bg-indigo-500/5' : 'text-slate-400 hover:text-slate-200'}">
                    {#if t.id !== 'all'}
                        <div class="w-2 h-2 rounded-full shrink-0" style="background:{colorFor(t.id)}"></div>
                    {/if}
                    {t.name}
                </button>
            {/each}
        </div>

        {#if sorted.length === 0}
            <div class="py-10 text-center text-slate-500 text-sm">No data for this section.</div>
        {:else}
            <table class="w-full text-sm">
                <thead>
                    <tr class="border-b border-slate-700 bg-slate-800/40">
                        {#each COLS as col}
                            <th
                                on:click={() => toggleSort(col.id)}
                                class="px-4 py-2.5 text-xs font-semibold text-slate-400 cursor-pointer select-none hover:text-slate-200 transition-colors
                                    {col.right ? 'text-right' : 'text-left'}">
                                <span class="inline-flex items-center gap-1 {col.right ? 'flex-row-reverse' : ''}">
                                    {col.label}
                                    {#if sortCol === col.id}
                                        <svg xmlns="http://www.w3.org/2000/svg" class="size-3 text-indigo-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                                            {#if sortDir === 'desc'}
                                                <polyline points="6 9 12 15 18 9"/>
                                            {:else}
                                                <polyline points="18 15 12 9 6 15"/>
                                            {/if}
                                        </svg>
                                    {:else}
                                        <svg xmlns="http://www.w3.org/2000/svg" class="size-3 opacity-25" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <polyline points="6 9 12 15 18 9"/>
                                        </svg>
                                    {/if}
                                </span>
                            </th>
                        {/each}
                    </tr>
                </thead>
                <tbody>
                    {#each sorted as task, i}
                        <tr class="border-b border-slate-800/60 transition-colors hover:bg-slate-700/20 {i % 2 !== 0 ? 'bg-slate-800/20' : ''}">
                            <td class="px-4 py-2.5">
                                <div class="flex items-center gap-2 min-w-0">
                                    <div class="w-2 h-2 rounded-full shrink-0" style="background:{colorFor(task.section_id)}"></div>
                                    <span class="text-slate-200 font-medium truncate">{task.title}</span>
                                    {#if activeTab === 'all' && task.section_name}
                                        <span class="text-xs text-slate-600 shrink-0 hidden sm:inline">{task.section_name}</span>
                                    {/if}
                                </div>
                            </td>
                            <td class="px-4 py-2.5 text-right tabular-nums {task.week_min ? 'text-slate-300' : 'text-slate-600'}">{fmt(task.week_min)}</td>
                            <td class="px-4 py-2.5 text-right tabular-nums font-medium {task.total_min ? 'text-slate-100' : 'text-slate-600'}">{fmt(task.total_min)}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        {/if}
    </div>
</div>
