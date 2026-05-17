<script>
    import { createEventDispatcher } from 'svelte';
    export let open = false;
    export let items = [];

    const dispatch = createEventDispatcher();

    let checked = {};

    $: if (open) {
        checked = Object.fromEntries(items.map(i => [i.task.id, false]));
    }

    $: anyChecked = Object.values(checked).some(Boolean);

    function pct(item) {
        return Math.min(100, Math.round((item.total_session_min / item.task.min_duration_min) * 100));
    }

    function fmtMin(m) {
        if (m < 60) return `${Math.round(m)}m`;
        const h = Math.floor(m / 60), r = Math.round(m % 60);
        return r > 0 ? `${h}h ${r}m` : `${h}h`;
    }

    function save() {
        const completions = items
            .filter(i => checked[i.task.id])
            .map(i => ({ taskId: i.task.id, date: i.latest_session_date }));
        dispatch('save', { completions });
    }

    function skip() {
        dispatch('skip');
    }
</script>

{#if open}
    <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60">
        <div class="bg-slate-900 border border-slate-700 rounded-xl shadow-2xl w-full max-w-md flex flex-col max-h-[85vh]">
            <div class="flex items-start justify-between p-4 border-b border-slate-700 shrink-0">
                <div>
                    <h2 class="text-base font-semibold text-slate-100">Review Recent Work</h2>
                    <p class="text-xs text-slate-400 mt-0.5">These tasks had time logged but didn't reach their minimum. Count them as done?</p>
                </div>
            </div>

            <div class="overflow-y-auto flex-1 p-4 space-y-3">
                {#each items as item (item.task.id)}
                    {@const p = pct(item)}
                    <label class="flex items-start gap-3 cursor-pointer group">
                        <input type="checkbox" bind:checked={checked[item.task.id]}
                            class="mt-1 shrink-0 accent-indigo-500 w-4 h-4 cursor-pointer" />
                        <div class="flex-1 min-w-0">
                            <div class="flex items-baseline justify-between gap-2">
                                <span class="text-sm font-medium text-slate-200 truncate">{item.task.title}</span>
                                <span class="text-xs text-slate-500 shrink-0">{item.latest_session_date}</span>
                            </div>
                            <div class="mt-1.5 h-1.5 rounded-full bg-slate-700 overflow-hidden">
                                <div class="h-full rounded-full {p >= 50 ? 'bg-amber-500' : 'bg-slate-500'}"
                                    style="width: {p}%"></div>
                            </div>
                            <div class="flex items-center justify-between mt-1">
                                <span class="text-xs text-slate-500">
                                    {fmtMin(item.total_session_min)} worked · {fmtMin(item.task.min_duration_min)} minimum
                                </span>
                                {#if p >= 50}
                                    <span class="text-xs text-amber-500">Close — you decide</span>
                                {/if}
                            </div>
                        </div>
                    </label>
                {/each}
            </div>

            <div class="flex gap-2 p-4 border-t border-slate-700 shrink-0">
                <button
                    on:click={save}
                    disabled={!anyChecked}
                    class="flex-1 py-2 text-sm font-semibold bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed text-white rounded-lg transition-colors">
                    Mark Selected Done
                </button>
                <button
                    on:click={skip}
                    class="px-4 py-2 text-sm text-slate-400 hover:text-slate-200 transition-colors">
                    Skip
                </button>
            </div>
        </div>
    </div>
{/if}
