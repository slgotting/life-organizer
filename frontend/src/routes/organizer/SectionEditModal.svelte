<script>
    import { createEventDispatcher } from 'svelte';
    export let open = false;
    export let section = null;

    const dispatch = createEventDispatcher();

    const DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const MODES = [
        { value: 'time_block', label: 'Time Block', active: 'bg-indigo-600 text-white' },
        { value: 'duration',   label: 'Duration',   active: 'bg-teal-700 text-white'   },
        { value: 'off',        label: 'Off',        active: 'bg-slate-600 text-slate-300' },
    ];

    let editName = '';
    let days = [];

    // Track a version key so initialization only fires when open/section actually
    // change, not on every parent re-render that re-passes the same prop values.
    let _initKey = null;
    $: _key = open ? (section?.id ?? '_') : null;
    $: if (_key !== _initKey) {
        _initKey = _key;
        if (open && section) {
            editName = section.name ?? '';
            days = Array.from({ length: 7 }, (_, i) => {
                const cfg = (section.day_configs ?? {})[String(i)] ?? {};
                return {
                    day: i,
                    mode: cfg.mode ?? 'off',
                    start_hour: cfg.start_hour ?? 9,
                    end_hour: cfg.end_hour ?? 17,
                    duration_min: cfg.duration_min ?? 120,
                };
            });
        }
    }

    function hour12(h) {
        if (h === 0) return '12am';
        if (h < 12) return `${h}am`;
        if (h === 12) return '12pm';
        return `${h - 12}pm`;
    }

    function fmtDuration(m) {
        const h = Math.floor(m / 60), rem = m % 60;
        return h && rem ? `${h}h ${rem}m` : h ? `${h}h` : `${rem}m`;
    }

    function copyToAll(i) {
        const src = days[i];
        days = days.map((d, j) => j === i ? d : { ...src, day: d.day });
    }

    function save() {
        if (!editName.trim()) return;
        const day_configs = {};
        for (const d of days) {
            if (d.mode === 'off') continue;
            day_configs[String(d.day)] = d.mode === 'time_block'
                ? { mode: 'time_block', start_hour: d.start_hour, end_hour: d.end_hour }
                : { mode: 'duration', duration_min: d.duration_min };
        }
        dispatch('save', { ...section, name: editName.trim(), day_configs });
    }
</script>

{#if open}
    <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60" on:click|self={() => dispatch('close')}>
        <div class="bg-slate-900 border border-slate-700 rounded-xl shadow-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
            <div class="flex items-center justify-between px-5 py-4 border-b border-slate-700">
                <h2 class="font-semibold text-slate-100">Section Schedule</h2>
                <button on:click={() => dispatch('close')} class="text-slate-400 hover:text-slate-200">
                    <svg xmlns="http://www.w3.org/2000/svg" class="size-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                </button>
            </div>

            <div class="px-5 py-4 space-y-4">
                <div>
                    <label class="block text-xs text-slate-400 mb-1">Name</label>
                    <input bind:value={editName} class="w-full bg-slate-800 border border-slate-600 rounded px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500" />
                </div>

                <div class="divide-y divide-slate-800">
                    {#each days as d, i}
                        <div class="group grid grid-cols-[2.5rem_1fr] gap-3 py-3">
                            <div class="flex flex-col items-center gap-1.5 pt-1">
                                <span class="text-xs font-medium text-slate-400">{DAY_NAMES[d.day]}</span>
                                <button
                                    on:click={() => copyToAll(i)}
                                    title="Copy to all days"
                                    class="opacity-0 group-hover:opacity-100 transition-opacity text-slate-600 hover:text-indigo-400">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                                    </svg>
                                </button>
                            </div>

                            <div class="space-y-2">
                                <div class="flex gap-1">
                                    {#each MODES as m}
                                        <button
                                            on:click={() => { days[i] = { ...days[i], mode: m.value }; }}
                                            class="flex-1 py-1 text-xs rounded transition-colors
                                                {d.mode === m.value
                                                    ? m.active
                                                    : 'bg-slate-800 text-slate-500 hover:bg-slate-700 hover:text-slate-300'}">
                                            {m.label}
                                        </button>
                                    {/each}
                                </div>

                                {#if d.mode === 'time_block'}
                                    <div class="flex items-center gap-2">
                                        <input type="range" min="0" max="23" bind:value={d.start_hour} class="flex-1 accent-indigo-500" />
                                        <span class="text-xs text-slate-300 w-10 text-right">{hour12(d.start_hour)}</span>
                                        <span class="text-xs text-slate-500">–</span>
                                        <input type="range" min="0" max="23" bind:value={d.end_hour} class="flex-1 accent-indigo-500" />
                                        <span class="text-xs text-slate-300 w-10 text-right">{hour12(d.end_hour)}</span>
                                    </div>
                                {:else if d.mode === 'duration'}
                                    <div class="flex items-center gap-2">
                                        <input type="range" min="15" max="480" step="15" bind:value={d.duration_min} class="flex-1 accent-teal-500" />
                                        <span class="text-xs text-slate-300 w-14 text-right">{fmtDuration(d.duration_min)}</span>
                                    </div>
                                {/if}
                            </div>
                        </div>
                    {/each}
                </div>
            </div>

            <div class="flex gap-2 px-5 py-4 border-t border-slate-700">
                <button on:click={() => dispatch('close')} class="flex-1 py-2 text-sm bg-slate-700 hover:bg-slate-600 text-slate-200 rounded transition-colors">Cancel</button>
                <button on:click={save} disabled={!editName.trim()} class="flex-1 py-2 text-sm bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white rounded font-semibold transition-colors">Save</button>
            </div>
        </div>
    </div>
{/if}
