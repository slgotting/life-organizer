<script>
    import { createEventDispatcher } from 'svelte';
    export let open = false;
    export let task = null;
    export let sections = [];
    export let presetScheduleType = null;

    const dispatch = createEventDispatcher();

    const DEFAULTS = {
        title: '', description: '', section_id: '', task_type: 'deep',
        priority: 'medium',
        min_duration_min: 60, max_duration_min: 120,
        recurrence_min_days: 2, recurrence_max_days: 5,
        overtime_eligible: false,
        is_one_off: false,
        pinned_dates: [],
        _newDate: '',
        schedule_type: 'recurring',
        scheduled_days: [],
        daily_target_min: 90,
        daily_target_manual: false,
    };

    const PRIORITIES = [
        { value: 'high',   label: 'High',   active: 'bg-rose-700 text-white',   idle: 'bg-slate-700 text-rose-300 hover:bg-slate-600'   },
        { value: 'medium', label: 'Medium', active: 'bg-slate-600 text-white',   idle: 'bg-slate-700 text-slate-300 hover:bg-slate-600'  },
        { value: 'low',    label: 'Low',    active: 'bg-slate-700 text-slate-300', idle: 'bg-slate-700 text-slate-500 hover:bg-slate-600' },
    ];

    const DAYS = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];

    let form = { ...DEFAULTS };
    let _initKey = null;
    $: _key = open ? (task?.id ?? '_new') : null;
    $: if (_key !== _initKey) {
        _initKey = _key;
        if (open) form = task
            ? { ...DEFAULTS, ...task, pinned_dates: [...(task.pinned_dates ?? [])], scheduled_days: [...(task.scheduled_days ?? [])], _newDate: '' }
            : { ...DEFAULTS, schedule_type: presetScheduleType || 'recurring' };
    }

    let autoTimer = null;
    let targetPulse = false;
    $: currentMode = form.is_one_off ? 'one_off' : (form.schedule_type || 'recurring');
    $: if (form.schedule_type === 'deep_work' && !form.daily_target_manual) {
        clearTimeout(autoTimer);
        autoTimer = setTimeout(() => {
            const v = Math.round((form.min_duration_min + form.max_duration_min) / 2);
            if (v !== form.daily_target_min) {
                form.daily_target_min = v;
                targetPulse = true;
                setTimeout(() => targetPulse = false, 600);
            }
        }, 1000);
    }

    function setScheduleMode(mode) {
        if (mode === 'one_off') {
            form.is_one_off = true;
            form.schedule_type = 'recurring';
        } else {
            form.is_one_off = false;
            form.schedule_type = mode;
        }
    }

    function toggleDay(i) {
        if (form.scheduled_days.includes(i)) {
            form.scheduled_days = form.scheduled_days.filter(d => d !== i);
        } else {
            form.scheduled_days = [...form.scheduled_days, i].sort((a, b) => a - b);
        }
    }

    function submit() {
        if (!form.title.trim()) return;
        if (form.schedule_type === 'deep_work' && form.scheduled_days.length === 0) return;
        dispatch('save', { ...form });
    }

    function clamp(field, min, max) {
        return (e) => {
            let v = parseInt(e.target.value);
            if (isNaN(v)) v = min;
            form[field] = Math.max(min, Math.min(max, v));
        };
    }

    function stepField(field, delta, min = 1) {
        form[field] = Math.max(min, (form[field] || 0) + delta);
    }
</script>

{#if open}
    <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60" on:click|self={() => dispatch('close')}>
        <div class="bg-slate-900 border border-slate-700 rounded-xl shadow-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
            <div class="flex items-center justify-between px-5 py-4 border-b border-slate-700">
                <h2 class="font-semibold text-slate-100">{task ? 'Edit Task' : 'New Task'}</h2>
                <button on:click={() => dispatch('close')} class="text-slate-400 hover:text-slate-200">
                    <svg xmlns="http://www.w3.org/2000/svg" class="size-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                </button>
            </div>

            <div class="px-5 py-4 space-y-4">
                <div>
                    <label class="block text-xs text-slate-400 mb-1">Title *</label>
                    <input bind:value={form.title} class="w-full bg-slate-800 border border-slate-600 rounded px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500" placeholder="Task title" />
                </div>

                <div>
                    <label class="block text-xs text-slate-400 mb-1">Schedule Type</label>
                    <div class="flex gap-0.5 rounded-lg bg-slate-800 border border-slate-600 p-0.5">
                        {#each [['recurring','Recurring'], ['deep_work','Fixed'], ['one_off','One-off']] as [val, label]}
                            <button
                                on:click={() => setScheduleMode(val)}
                                class="flex-1 py-1.5 text-xs rounded font-medium transition-colors
                                    {currentMode === val ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'}">
                                {label}
                            </button>
                        {/each}
                    </div>
                </div>

                <div>
                    <label class="block text-xs text-slate-400 mb-1">Description</label>
                    <textarea bind:value={form.description} rows="2" class="w-full bg-slate-800 border border-slate-600 rounded px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500 resize-none" placeholder="Optional details..."></textarea>
                </div>

                <div>
                    <label class="block text-xs text-slate-400 mb-1">Section</label>
                    <select bind:value={form.section_id} class="w-full bg-slate-800 border border-slate-600 rounded px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500">
                        <option value="">None</option>
                        {#each sections as s}
                            <option value={s.id}>{s.name}</option>
                        {/each}
                    </select>
                </div>

                <div>
                    <label class="block text-xs text-slate-400 mb-1">Priority</label>
                    <div class="flex gap-1">
                        {#each PRIORITIES as p}
                            <button
                                on:click={() => form.priority = p.value}
                                class="flex-1 py-1.5 text-xs rounded font-medium transition-colors {form.priority === p.value ? p.active : p.idle}">
                                {p.label}
                            </button>
                        {/each}
                    </div>
                </div>

                <div>
                    <label class="block text-xs text-slate-400 mb-2">Duration Range (minutes)</label>
                    <div class="flex items-center gap-2">
                        <div class="flex items-center gap-1">
                            <button on:click={() => stepField('min_duration_min', -15)} class="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs">−</button>
                            <input type="number" bind:value={form.min_duration_min} on:change={clamp('min_duration_min', 5, 480)} class="w-16 text-center bg-slate-800 border border-slate-600 rounded px-2 py-1 text-sm text-slate-100 focus:outline-none focus:border-indigo-500" />
                            <button on:click={() => stepField('min_duration_min', 15)} class="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs">+</button>
                        </div>
                        <span class="text-slate-500 text-xs">to</span>
                        <div class="flex items-center gap-1">
                            <button on:click={() => stepField('max_duration_min', -15)} class="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs">−</button>
                            <input type="number" bind:value={form.max_duration_min} on:change={clamp('max_duration_min', 5, 480)} class="w-16 text-center bg-slate-800 border border-slate-600 rounded px-2 py-1 text-sm text-slate-100 focus:outline-none focus:border-indigo-500" />
                            <button on:click={() => stepField('max_duration_min', 15)} class="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs">+</button>
                        </div>
                        {#if form.schedule_type === 'deep_work'}
                            <span class="text-slate-500 text-xs ml-1">target:</span>
                            <input
                                type="number"
                                bind:value={form.daily_target_min}
                                on:input={() => { form.daily_target_manual = true; }}
                                min="1"
                                class="w-16 text-center bg-slate-800 border rounded px-2 py-1 text-sm text-slate-100 focus:outline-none focus:border-indigo-500
                                    {form.daily_target_manual ? 'border-slate-600' : 'border-emerald-700/60'}
                                    {targetPulse ? 'pulse-once' : ''}" />
                            <span class="text-slate-500 text-xs">m/day</span>
                            {#if form.daily_target_manual}
                                <button
                                    on:click={() => { form.daily_target_manual = false; form.daily_target_min = Math.round((form.min_duration_min + form.max_duration_min) / 2); }}
                                    class="text-xs text-emerald-500 hover:text-emerald-400 whitespace-nowrap">↺ auto</button>
                            {:else}
                                <span class="text-xs text-emerald-600 italic">auto</span>
                            {/if}
                        {/if}
                    </div>
                </div>

                {#if form.schedule_type === 'deep_work'}
                    <div>
                        <label class="block text-xs text-slate-400 mb-1">Active Days</label>
                        <div class="flex gap-1">
                            {#each DAYS as label, i}
                                <button
                                    on:click={() => toggleDay(i)}
                                    class="flex-1 py-2 text-xs rounded font-medium transition-colors
                                        {form.scheduled_days.includes(i) ? 'bg-emerald-700 text-white' : 'bg-slate-700 text-slate-400 hover:bg-slate-600'}">
                                    {label}
                                </button>
                            {/each}
                        </div>
                        {#if form.scheduled_days.length === 0}
                            <p class="text-xs text-rose-400 mt-1">Select at least one day.</p>
                        {/if}
                    </div>
                {/if}

                {#if form.schedule_type === 'recurring' && !form.is_one_off}
                    <div>
                        <label class="block text-xs text-slate-400 mb-2">Recurrence (days between doing)</label>
                        <div class="flex items-center gap-2">
                            <div class="flex items-center gap-1">
                                <button on:click={() => stepField('recurrence_min_days', -1)} class="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs">−</button>
                                <input type="number" bind:value={form.recurrence_min_days} class="w-14 text-center bg-slate-800 border border-slate-600 rounded px-2 py-1 text-sm text-slate-100 focus:outline-none focus:border-indigo-500" />
                                <button on:click={() => stepField('recurrence_min_days', 1)} class="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs">+</button>
                            </div>
                            <span class="text-slate-500 text-xs">to</span>
                            <div class="flex items-center gap-1">
                                <button on:click={() => stepField('recurrence_max_days', -1)} class="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs">−</button>
                                <input type="number" bind:value={form.recurrence_max_days} class="w-14 text-center bg-slate-800 border border-slate-600 rounded px-2 py-1 text-sm text-slate-100 focus:outline-none focus:border-indigo-500" />
                                <button on:click={() => stepField('recurrence_max_days', 1)} class="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs">+</button>
                            </div>
                        </div>
                    </div>
                {/if}

                <label class="flex items-center gap-2 cursor-pointer">
                    <input type="checkbox" bind:checked={form.overtime_eligible} class="w-4 h-4 rounded accent-indigo-500" />
                    <span class="text-sm text-slate-300">Allow overtime scheduling (extend into non-work hours when urgent)</span>
                </label>

                <div>
                    <label class="block text-xs text-slate-400 mb-1">Schedule for specific days (optional)</label>
                    <div class="flex gap-2">
                        <input
                            type="date"
                            bind:value={form._newDate}
                            class="flex-1 bg-slate-800 border border-slate-600 rounded px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500 [color-scheme:dark]" />
                        <button
                            type="button"
                            on:click={() => { if (form._newDate && !form.pinned_dates.includes(form._newDate)) { form.pinned_dates = [...form.pinned_dates, form._newDate].sort(); form._newDate = ''; } }}
                            class="px-3 py-1.5 text-xs bg-indigo-700 hover:bg-indigo-600 text-white rounded transition-colors">
                            Add
                        </button>
                    </div>
                    {#if form.pinned_dates.length > 0}
                        <div class="flex flex-wrap gap-1.5 mt-2">
                            {#each form.pinned_dates as d}
                                <span class="flex items-center gap-1 px-2 py-0.5 bg-indigo-900/40 border border-indigo-700/50 rounded text-xs text-indigo-300">
                                    {d}
                                    <button type="button" on:click={() => form.pinned_dates = form.pinned_dates.filter(x => x !== d)} class="text-indigo-500 hover:text-rose-400 transition-colors">×</button>
                                </span>
                            {/each}
                        </div>
                    {/if}
                </div>
            </div>

            <div class="flex gap-2 px-5 py-4 border-t border-slate-700">
                <button on:click={() => dispatch('close')} class="flex-1 py-2 text-sm bg-slate-700 hover:bg-slate-600 text-slate-200 rounded transition-colors">Cancel</button>
                <button on:click={submit} disabled={!form.title.trim() || (form.schedule_type === 'deep_work' && form.scheduled_days.length === 0)} class="flex-1 py-2 text-sm bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white rounded font-semibold transition-colors">
                    {task ? 'Save Changes' : 'Create Task'}
                </button>
            </div>
        </div>
    </div>
{/if}

<style>
    @keyframes pulse-once {
        0%   { transform: scale(1);    opacity: 1; }
        40%  { transform: scale(1.07); opacity: 0.7; }
        100% { transform: scale(1);    opacity: 1; }
    }
    :global(.pulse-once) {
        animation: pulse-once 0.5s ease-out;
    }
</style>
