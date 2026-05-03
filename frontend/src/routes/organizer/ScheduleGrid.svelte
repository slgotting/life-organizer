<script>
    export let schedule = [];
    export let sections = [];

    const URGENCY_COLORS = {
        upcoming:    'bg-slate-700 text-slate-300',
        needs_doing: 'bg-yellow-900 text-yellow-300',
        time_to_do:  'bg-orange-900 text-orange-300',
        overdue:     'bg-red-900 text-red-300',
    };

    const SECTION_PALETTE = [
        { leftBorder: 'border-indigo-500', label: 'text-indigo-400' },
        { leftBorder: 'border-violet-500', label: 'text-violet-400' },
        { leftBorder: 'border-cyan-500',   label: 'text-cyan-400'   },
        { leftBorder: 'border-teal-500',   label: 'text-teal-400'   },
        { leftBorder: 'border-amber-500',  label: 'text-amber-400'  },
        { leftBorder: 'border-rose-500',   label: 'text-rose-400'   },
    ];

    function paletteFor(sectionId) {
        const idx = sections.findIndex(s => s.id === sectionId);
        return SECTION_PALETTE[Math.max(0, idx) % SECTION_PALETTE.length];
    }

    function groupBySection(tasks) {
        const map = new Map();
        for (const t of tasks) {
            const sid = t.section_id || '';
            if (!map.has(sid)) map.set(sid, []);
            map.get(sid).push(t);
        }
        return [...map.entries()]
            .map(([sid, ts]) => ({
                sectionId: sid,
                section: sections.find(s => s.id === sid) ?? null,
                tasks: ts,
                palette: paletteFor(sid),
            }))
            .sort((a, b) => {
                const ai = sections.findIndex(s => s.id === a.sectionId);
                const bi = sections.findIndex(s => s.id === b.sectionId);
                return (ai === -1 ? 999 : ai) - (bi === -1 ? 999 : bi);
            });
    }

    function fmtRange(min, max) {
        return min === max ? `${min}m` : `${min}–${max}m`;
    }

    function pct(scheduled, available) {
        if (!available) return 0;
        return Math.min(100, Math.round((scheduled / available) * 100));
    }
</script>

<div class="grid grid-cols-7 gap-1.5">
    {#each schedule as day}
        <div class="rounded-lg border {day.overloaded ? 'border-red-700/60 bg-red-900/10' : day.is_work_day ? 'border-slate-700 bg-slate-800/40' : 'border-slate-800 bg-slate-900/20'} p-2 min-h-[120px]">
            <div class="mb-1.5">
                <div class="text-xs font-semibold {day.overloaded ? 'text-red-400' : 'text-slate-300'}">{day.day_name.slice(0, 3)}</div>
                <div class="text-xs text-slate-500">{day.date.slice(5)}</div>
            </div>

            {#if day.is_work_day && day.available_min > 0}
                <div class="w-full h-1 bg-slate-700 rounded-full mb-2">
                    <div
                        class="h-1 rounded-full transition-all {day.overloaded ? 'bg-red-500' : 'bg-indigo-500'}"
                        style="width: {pct(day.total_scheduled_min, day.available_min)}%">
                    </div>
                </div>
            {/if}

            {#if day.tasks.length === 0 && day.is_work_day}
                <span class="text-xs text-slate-600 italic">Free</span>
            {:else if !day.is_work_day}
                <span class="text-xs text-slate-700 italic">Off</span>
            {:else}
                <div class="space-y-1.5">
                    {#each groupBySection(day.tasks) as group}
                        <div class="border-l-2 {group.section ? group.palette.leftBorder : 'border-slate-600'} pl-1 space-y-0.5">
                            {#if group.section}
                                <div class="text-[9px] font-semibold {group.palette.label} truncate leading-tight">{group.section.name}</div>
                            {/if}
                            {#each group.tasks as t}
                                <div class="px-1 py-0.5 rounded text-xs {URGENCY_COLORS[t.urgency] ?? URGENCY_COLORS.upcoming} truncate" title="{t.title} · {fmtRange(t.min_duration_min, t.max_duration_min)}">
                                    {t.title}
                                </div>
                            {/each}
                        </div>
                    {/each}
                </div>
            {/if}
        </div>
    {/each}
</div>
