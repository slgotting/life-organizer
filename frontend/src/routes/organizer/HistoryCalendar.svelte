<script>
    import { createEventDispatcher } from 'svelte';
    export let sessions = [];
    export let timeBlocks = {};
    export let sections = [];
    export let days = [];
    export let tasks = [];

    const dispatch = createEventDispatcher();

    const PALETTE = [
        { bg: 'rgba(99,102,241,0.08)',  border: 'rgba(99,102,241,0.22)', task: 'rgba(79,70,229,0.88)',   text: '#e0e7ff' },
        { bg: 'rgba(139,92,246,0.08)',  border: 'rgba(139,92,246,0.22)', task: 'rgba(124,58,237,0.88)',  text: '#ede9fe' },
        { bg: 'rgba(6,182,212,0.08)',   border: 'rgba(6,182,212,0.22)',  task: 'rgba(8,145,178,0.88)',   text: '#cffafe' },
        { bg: 'rgba(20,184,166,0.08)',  border: 'rgba(20,184,166,0.22)', task: 'rgba(15,118,110,0.88)',  text: '#ccfbf1' },
        { bg: 'rgba(245,158,11,0.08)',  border: 'rgba(245,158,11,0.22)', task: 'rgba(217,119,6,0.88)',   text: '#fef3c7' },
        { bg: 'rgba(244,63,94,0.08)',   border: 'rgba(244,63,94,0.22)',  task: 'rgba(225,29,72,0.88)',   text: '#ffe4e6' },
    ];

    function paletteFor(sectionId) {
        const idx = sections.findIndex(s => s.id === sectionId);
        return PALETTE[Math.max(0, idx) % PALETTE.length];
    }

    let minHour = 8, maxHour = 18;
    $: {
        let mn = 23, mx = 1, found = false;
        for (const blocks of Object.values(timeBlocks)) {
            for (const b of blocks) { mn = Math.min(mn, b.start_hour); mx = Math.max(mx, b.end_hour); found = true; }
        }
        for (const s of sessions) {
            const st = new Date(s.start_time + 'Z'), en = new Date(s.end_time + 'Z');
            mn = Math.min(mn, st.getHours());
            mx = Math.max(mx, en.getHours() + (en.getMinutes() > 0 ? 1 : 0));
            found = true;
        }
        if (found) { minHour = Math.max(0, mn); maxHour = Math.min(24, mx + 1); }
    }

    $: totalHours = Math.max(maxHour - minHour, 1);
    $: hourTicks = Array.from({ length: totalHours + 1 }, (_, i) => minHour + i);

    function top(h)            { return `${(h - minHour) / totalHours * 100}%`; }
    function blockHeight(s, e) { return `${Math.max((e - s) / totalHours * 100, 0.5)}%`; }

    function sessionsForDay(dateStr) {
        const mapped = sessions
            .filter(s => new Date(s.start_time + 'Z').toLocaleDateString('en-CA') === dateStr)
            .map(s => {
                const st = new Date(s.start_time + 'Z'), en = new Date(s.end_time + 'Z');
                return { ...s, startH: st.getHours() + st.getMinutes() / 60, endH: en.getHours() + en.getMinutes() / 60, startDate: st, endDate: en };
            })
            .sort((a, b) => a.startH - b.startH);
        const out = [];
        let i = 0;
        while (i < mapped.length) {
            const cur = { ...mapped[i], _sessions: [mapped[i]] };
            while (i + 1 < mapped.length) {
                const nxt = mapped[i + 1];
                const gapMin = (nxt.startH - cur.endH) * 60;
                if (nxt.task_id !== cur.task_id || gapMin < 0 || gapMin >= 5) break;
                const otherInGap = mapped.some(
                    x => x.id !== cur.id && x.id !== nxt.id && x.task_id !== cur.task_id
                      && x.startH >= cur.endH && x.startH < nxt.startH
                );
                if (otherInGap) break;
                if (nxt.endH > cur.endH) cur.endDate = nxt.endDate;
                cur.endH = Math.max(cur.endH, nxt.endH);
                cur.duration_min = (cur.duration_min || 0) + (nxt.duration_min || 0);
                cur._sessions = [...cur._sessions, nxt];
                i++;
            }
            out.push(cur);
            i++;
        }
        return out;
    }

    function fmtHour(h) {
        const ampm = h < 12 ? 'am' : 'pm';
        return `${h % 12 || 12}${ampm}`;
    }

    function fmtTime(date) {
        return date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
    }

    function fmtDuration(min) {
        if (min < 60) return `${min}m`;
        const h = Math.floor(min / 60), m = min % 60;
        return m ? `${h}h ${m}m` : `${h}h`;
    }

    // Edit popover state
    let popover = null;
    let editSessions = [];

    // Create popover state
    let createPopover = null;
    let createTaskId = '';
    let createStart = '';
    let createEnd = '';

    $: createDurationMin = (createStart && createEnd && new Date(createEnd) > new Date(createStart))
        ? Math.round((new Date(createEnd) - new Date(createStart)) / 60000)
        : null;

    function onColumnClick(e, day) {
        if (e.target.closest('[role="button"]')) return;
        e.stopPropagation();
        const MARGIN = 12, W = 260, H = 300;
        let x = e.clientX + MARGIN;
        let y = e.clientY + MARGIN;
        if (x + W > window.innerWidth  - MARGIN) x = e.clientX - W - MARGIN;
        if (y + H > window.innerHeight - MARGIN) y = e.clientY - H - MARGIN;
        const rect = e.currentTarget.getBoundingClientRect();
        const ratio = Math.max(0, Math.min(1, (e.clientY - rect.top) / rect.height));
        const clickedHour = minHour + ratio * totalHours;
        const hour = Math.min(23, Math.floor(clickedHour));
        const min = Math.round(((clickedHour - hour) * 60) / 15) * 15;
        const pad = n => String(n).padStart(2, '0');
        const h2 = min >= 60 ? hour + 1 : hour;
        const m2 = min >= 60 ? 0 : min;
        createStart = `${day.dateStr}T${pad(h2)}:${pad(m2)}`;
        const endDate = new Date(`${day.dateStr}T${pad(h2)}:${pad(m2)}:00`);
        endDate.setMinutes(endDate.getMinutes() + 30);
        createEnd = `${endDate.getFullYear()}-${pad(endDate.getMonth()+1)}-${pad(endDate.getDate())}T${pad(endDate.getHours())}:${pad(endDate.getMinutes())}`;
        createTaskId = tasks[0]?.id ?? '';
        createPopover = { x, y };
    }

    function saveCreate() {
        if (!createTaskId || !createStart || !createEnd || !createDurationMin || createDurationMin <= 0) return;
        dispatch('createsession', {
            taskId: createTaskId,
            startTime: new Date(createStart).toISOString(),
            endTime: new Date(createEnd).toISOString(),
        });
        createPopover = null;
    }

    function toLocalDatetimeInput(utcIsoStr) {
        const d = new Date(utcIsoStr + 'Z');
        const pad = n => String(n).padStart(2, '0');
        return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
    }

    function openPopover(e, session) {
        e.stopPropagation();
        const MARGIN = 12, W = 240, H = 300;
        let x = e.clientX + MARGIN;
        let y = e.clientY + MARGIN;
        if (x + W > window.innerWidth  - MARGIN) x = e.clientX - W - MARGIN;
        if (y + H > window.innerHeight - MARGIN) y = e.clientY - H - MARGIN;
        popover = { session, x, y };
        editSessions = (session._sessions ?? [session]).map(s => ({
            id: s.id,
            editStart: toLocalDatetimeInput(s.start_time),
            editEnd: toLocalDatetimeInput(s.end_time),
        }));
    }

    function closePopover() { popover = null; createPopover = null; }

    function saveSessionEdit() {
        dispatch('updatesessions', editSessions.map(es => ({
            sessionId: es.id,
            startTime: new Date(es.editStart).toISOString(),
            endTime: new Date(es.editEnd).toISOString(),
        })));
        popover = null;
    }

    function deleteOneSession(id) {
        dispatch('deletesession', { sessionId: id });
        editSessions = editSessions.filter(es => es.id !== id);
        if (editSessions.length === 0) popover = null;
    }

    function onKeydown(e) { if (e.key === 'Escape') closePopover(); }
</script>

<svelte:window on:keydown={onKeydown} on:click={closePopover} />

<div class="flex flex-col h-full select-none">
    <!-- Day headers -->
    <div class="flex shrink-0 border-b border-slate-700 pb-1.5">
        <div class="w-10 shrink-0"></div>
        {#each days as day}
            <div class="flex-1 text-center min-w-0">
                <div class="text-xs font-semibold {day.isToday ? 'text-indigo-400' : 'text-slate-300'}">
                    {day.dayName.slice(0, 3)}
                </div>
                <div class="text-xs {day.isToday ? 'text-indigo-300' : 'text-slate-500'}">
                    {day.dateStr.slice(5)}
                </div>
            </div>
        {/each}
    </div>

    <!-- Grid body -->
    <div class="flex flex-1 min-h-0">
        <!-- Time labels -->
        <div class="w-10 shrink-0 relative">
            {#each hourTicks as h}
                <div
                    class="absolute right-1.5 text-slate-600 leading-none"
                    style="top: {top(h)}; font-size: 9px; transform: translateY(-50%);">
                    {fmtHour(h)}
                </div>
            {/each}
        </div>

        <!-- Day columns -->
        {#each days as day}
            <div class="flex-1 relative border-l border-slate-800 min-w-0 cursor-crosshair" on:click={(e) => onColumnClick(e, day)}>
                <!-- Hour grid lines -->
                {#each hourTicks as h}
                    <div
                        class="absolute left-0 right-0 border-t {h % 2 === 0 ? 'border-slate-800' : 'border-slate-800/40'}"
                        style="top: {top(h)};">
                    </div>
                {/each}

                <!-- Section time blocks -->
                {#each (timeBlocks[day.dateStr] ?? []) as block}
                    {@const p = paletteFor(block.section_id)}
                    <div
                        class="absolute left-0 right-0 pointer-events-none"
                        style="top: {top(block.start_hour)}; height: {blockHeight(block.start_hour, block.end_hour)}; background: {p.bg}; border-left: 2px solid {p.border};">
                        <span class="absolute top-0.5 left-1.5 font-medium opacity-60" style="font-size: 9px; color: {p.text};">
                            {block.section_name}
                        </span>
                    </div>
                {/each}

                <!-- Session blocks -->
                {#each sessionsForDay(day.dateStr) as s}
                    {@const p = paletteFor(s.section_id)}
                    {@const durationH = s.endH - s.startH}
                    <div
                        role="button"
                        tabindex="0"
                        on:click={(e) => openPopover(e, s)}
                        on:keydown={(e) => e.key === 'Enter' && openPopover(e, s)}
                        class="absolute left-px right-px rounded overflow-hidden flex flex-col px-1 py-0.5 cursor-pointer transition-opacity hover:opacity-80"
                        style="top: {top(s.startH)}; height: {blockHeight(s.startH, s.endH)}; background: {p.task};">
                        <span class="font-medium leading-tight truncate" style="font-size: 10px; color: {p.text};">
                            {s.task_title}
                        </span>
                        {#if durationH > 0.4}
                            <span class="leading-tight opacity-80" style="font-size: 9px; color: {p.text};">
                                {s.duration_min}m
                            </span>
                        {/if}
                    </div>
                {/each}
            </div>
        {/each}
    </div>
</div>

<!-- Popover -->
{#if popover}
    {@const s = popover.session}
    {@const p = paletteFor(s.section_id)}
    {@const multi = editSessions.length > 1}
    <div
        role="tooltip"
        on:click|stopPropagation
        class="fixed z-50 w-56 rounded-lg border border-slate-600 bg-slate-900 shadow-2xl p-3 space-y-2"
        style="left: {popover.x}px; top: {popover.y}px;">
        <div class="flex items-start justify-between gap-2">
            <span class="font-semibold text-slate-100 text-sm leading-snug">{s.task_title}</span>
            <button on:click={closePopover} class="shrink-0 text-slate-500 hover:text-slate-300 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
            </button>
        </div>
        {#if s.section_name}
            <div class="flex items-center gap-1.5">
                <div class="w-2 h-2 rounded-full shrink-0" style="background: {p.task};"></div>
                <span class="text-xs text-slate-400">{s.section_name}</span>
            </div>
        {/if}
        <div class="relative">
            <div
                class="space-y-3 overflow-y-auto pb-8"
                style="{editSessions.length >= 3 ? 'max-height: 230px;' : ''}">
                {#each editSessions as es, i}
                    <div class="space-y-1.5">
                        {#if multi}
                            <div class="flex items-center justify-between">
                                <span class="text-xs font-semibold text-slate-400">Block {i + 1}</span>
                                <button on:click={() => deleteOneSession(es.id)}
                                    class="text-slate-600 hover:text-red-400 transition-colors" title="Delete block">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="size-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/>
                                    </svg>
                                </button>
                            </div>
                        {/if}
                        <div class="space-y-0.5">
                            <label class="text-xs text-slate-500 block">Start</label>
                            <input type="datetime-local" bind:value={editSessions[i].editStart}
                                on:click|stopPropagation
                                class="w-full text-xs bg-slate-800 border border-slate-600 rounded px-2 py-1 text-slate-200 focus:outline-none focus:border-indigo-500" />
                        </div>
                        <div class="space-y-0.5">
                            <label class="text-xs text-slate-500 block">End</label>
                            <input type="datetime-local" bind:value={editSessions[i].editEnd}
                                on:click|stopPropagation
                                class="w-full text-xs bg-slate-800 border border-slate-600 rounded px-2 py-1 text-slate-200 focus:outline-none focus:border-indigo-500" />
                        </div>
                    </div>
                {/each}
            </div>
            {#if editSessions.length >= 3}
                <div class="absolute bottom-0 left-0 right-0 h-10 pointer-events-none rounded-b-sm"
                    style="background: linear-gradient(to bottom, transparent, rgba(15,23,42,0.95));"></div>
            {/if}
        </div>
        <div class="flex gap-1.5">
            <button on:click={saveSessionEdit}
                class="flex-1 text-xs bg-indigo-600 hover:bg-indigo-500 text-white rounded px-2 py-1 font-semibold transition-colors">
                Save
            </button>
            {#if !multi}
                <button on:click={() => deleteOneSession(editSessions[0].id)}
                    class="text-xs bg-slate-700 hover:bg-red-800 text-slate-400 hover:text-red-200 rounded px-2 py-1 transition-colors" title="Delete session">
                    <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/>
                    </svg>
                </button>
            {/if}
        </div>
    </div>
{/if}

{#if createPopover}
    <div
        role="dialog"
        on:click|stopPropagation
        class="fixed z-50 w-64 rounded-lg border border-slate-600 bg-slate-900 shadow-2xl p-3 space-y-2"
        style="left: {createPopover.x}px; top: {createPopover.y}px;">
        <div class="flex items-center justify-between">
            <span class="font-semibold text-slate-100 text-sm">Log Session</span>
            <button on:click={closePopover} class="shrink-0 text-slate-500 hover:text-slate-300 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
            </button>
        </div>
        <div class="space-y-0.5">
            <label class="text-xs text-slate-500 block">Task</label>
            <select bind:value={createTaskId} on:click|stopPropagation
                class="w-full text-xs bg-slate-800 border border-slate-600 rounded px-2 py-1 text-slate-200 focus:outline-none focus:border-indigo-500">
                {#each tasks as t}
                    <option value={t.id}>{t.title}</option>
                {/each}
            </select>
        </div>
        <div class="space-y-1.5">
            <div class="space-y-0.5">
                <label class="text-xs text-slate-500 block">Start</label>
                <input type="datetime-local" bind:value={createStart} on:click|stopPropagation
                    class="w-full text-xs bg-slate-800 border border-slate-600 rounded px-2 py-1 text-slate-200 focus:outline-none focus:border-indigo-500" />
            </div>
            <div class="space-y-0.5">
                <label class="text-xs text-slate-500 block">End</label>
                <input type="datetime-local" bind:value={createEnd} on:click|stopPropagation
                    class="w-full text-xs bg-slate-800 border border-slate-600 rounded px-2 py-1 text-slate-200 focus:outline-none focus:border-indigo-500" />
            </div>
            {#if createDurationMin !== null}
                <div class="text-xs text-slate-400">{fmtDuration(createDurationMin)}</div>
            {/if}
            <button on:click={saveCreate}
                disabled={!createTaskId || !createDurationMin || createDurationMin <= 0}
                class="w-full text-xs bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white rounded px-2 py-1 font-semibold transition-colors">
                Log Session
            </button>
        </div>
    </div>
{/if}
