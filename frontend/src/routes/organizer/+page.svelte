<script>
    import { onMount } from 'svelte';
    import toast from 'svelte-french-toast';
    import { goto } from '$app/navigation';
    import { authStore } from '../../stores/auth';
    import { activeSessionStore } from '../../stores/session';
    import config, { buildServerEndpoint } from '../../config/config';
    import { authenticatedJSONRequest } from '../../lib/auth';
    import { handleApiResponse } from '../../lib/api';
    import ActiveTimer from './ActiveTimer.svelte';
    import TaskCard from './TaskCard.svelte';
    import TaskModal from './TaskModal.svelte';
    import ScheduleGrid from './ScheduleGrid.svelte';
    import SectionsSidebar from './SectionsSidebar.svelte';
    import SectionEditModal from './SectionEditModal.svelte';
    import QuickAddModal from './QuickAddModal.svelte';
    import AssignDayModal from './AssignDayModal.svelte';
    import HistoryCalendar from './HistoryCalendar.svelte';
    import StatsPanel from './StatsPanel.svelte';

    if (!$authStore.isAuthenticated) goto('/signin');

    let tasks = [];
    let schedule = [];
    let sections = [];
    let overloadWarning = false;
    let atCapacity = false;
    let loading = true;
    let tab = 'today';

    let completingId = null;
    let taskModalOpen = false;

    $: activeSession = $activeSessionStore.session;
    $: activeTask = $activeSessionStore.task;
    $: activeTimerMin = $activeSessionStore.timerMin;

    // When a session is stopped externally (from another page), refresh task state
    let _prevSession = null;
    $: {
        const curr = $activeSessionStore.session;
        if (_prevSession && !curr && !loading) {
            api(config.organizerTasksEndpoint).then(res => { if (res?.success) tasks = res.tasks; });
            loadTodayMinutes();
            if (historyData) loadHistory();
        }
        _prevSession = curr;
    }
    let taskTodayMin = {};
    let editingTask = null;
    let quickAddOpen = false;
    let assignDayOpen = false;
    let weekDirty = false;
    let historyData = null;
    let historyLoading = false;
    let statsData = null;
    let statsLoading = false;
    let historyWeekStart = (() => {
        const d = new Date();
        d.setDate(d.getDate() - ((d.getDay() + 6) % 7));
        return d.toISOString().slice(0, 10);
    })();
    let selectedSectionId = null;
    let sectionEditOpen = false;
    let editingSection = null;

    function token() {
        return JSON.parse(localStorage.getItem('auth'))?.token;
    }

    async function api(endpoint, method = 'GET', data = undefined) {
        const res = await authenticatedJSONRequest(buildServerEndpoint(endpoint), method, token(), data);
        return handleApiResponse(res);
    }

    function currentWeekStart() {
        const d = new Date();
        d.setDate(d.getDate() - ((d.getDay() + 6) % 7));
        return d.toISOString().slice(0, 10);
    }

    async function loadTodayMinutes() {
        const res = await api(`${config.organizerHistoryEndpoint}?week_start=${currentWeekStart()}`);
        if (!res?.success) return;
        const todayStr = new Date().toLocaleDateString('en-CA');
        const map = {};
        for (const s of res.sessions) {
            const sDate = new Date(s.start_time + 'Z').toLocaleDateString('en-CA');
            if (sDate === todayStr) map[s.task_id] = (map[s.task_id] || 0) + (s.duration_min || 0);
        }
        taskTodayMin = map;
    }

    async function loadAll() {
        loading = true;
        try {
            const [tRes, sRes, sectRes, sessRes, capRes] = await Promise.all([
                api(config.organizerTasksEndpoint),
                api(config.organizerScheduleEndpoint + `?days=7&tz_offset=${new Date().getTimezoneOffset()}`),
                api(config.organizerSectionsEndpoint),
                api(config.organizerActiveSessionEndpoint),
                api(config.organizerCapacityEndpoint),
            ]);
            if (tRes?.success)    tasks = tRes.tasks;
            if (sRes?.success)    { schedule = sRes.schedule; overloadWarning = sRes.overload_warning; }
            if (sectRes?.success) sections = sectRes.sections;
            if (sessRes?.success) {
                const timerMin = sessRes.session
                    ? (JSON.parse(localStorage.getItem('activeTimerMin') || 'null')?.sessionId === sessRes.session.id
                        ? JSON.parse(localStorage.getItem('activeTimerMin')).timerMin : null)
                    : null;
                activeSessionStore.set({ session: sessRes.session, task: sessRes.task ?? null, timerMin });
            }
            if (capRes?.success)  atCapacity = capRes.at_capacity;
        } finally {
            loading = false;
        }
        loadTodayMinutes();
    }

    onMount(loadAll);

    async function startTask({ task, timerMin = null }) {
        if (activeSession && activeSession.task_id !== task.id) {
            if (!confirm(`Stop "${activeTask?.title ?? 'current task'}" to start "${task.title}"?`)) return;
            await stopTask();
        }
        const res = await api(`${config.organizerTasksEndpoint}/${task.id}/start`, 'POST');
        if (res?.success) {
            if (timerMin !== null) {
                localStorage.setItem('activeTimerMin', JSON.stringify({ sessionId: res.session.id, timerMin }));
            } else {
                localStorage.removeItem('activeTimerMin');
            }
            activeSessionStore.set({ session: res.session, task, timerMin });
            toast.success(`Started: ${task.title}`);
        } else {
            toast.error(res?.message ?? 'Could not start task');
        }
    }

    async function quickAddTask(e) {
        const { data, startNow } = e.detail;
        const res = await api(config.organizerTasksEndpoint, 'POST', data);
        if (!res?.success) { toast.error('Could not create task'); return; }
        tasks = [...tasks, res.task];
        quickAddOpen = false;
        if (startNow && !activeSession) {
            await startTask({ task: res.task, timerMin: null });
        } else {
            await refreshSchedule();
            toast.success('Task added!');
        }
    }

    async function skipTask(task) {
        const res = await api(`${config.organizerTasksEndpoint}/${task.id}/snooze`, 'POST');
        if (res?.success) {
            await refreshSchedule();
            toast.success(`"${task.title}" pushed to tomorrow`);
        }
    }

    async function assignTaskToDay(e) {
        const { taskId, date } = e.detail;
        const task = tasks.find(t => t.id === taskId);
        if (!task) return;
        const current = task.pinned_dates ?? [];
        const removing = current.includes(date);
        const pinned_dates = removing ? current.filter(d => d !== date) : [...current, date];
        const res = await api(`${config.organizerTasksEndpoint}/${taskId}`, 'PUT', { pinned_dates });
        if (res?.success) {
            tasks = tasks.map(t => t.id === taskId ? res.task : t);
            await refreshSchedule();
            toast.success(removing ? `"${task.title}" removed from ${date}` : `"${task.title}" scheduled for ${date}`);
        }
    }

    async function assignFromWeekGrid(e) {
        const { taskId, date: targetDate, sourceDate } = e.detail;
        const task = tasks.find(t => t.id === taskId);
        if (!task) return;

        const current = task.pinned_dates ?? [];
        const pinned_dates = [...current.filter(d => d !== sourceDate), ...(current.includes(targetDate) ? [] : [targetDate])];

        const scheduleTask = { id: task.id, title: task.title, urgency: task.urgency, priority: task.priority, section_id: task.section_id, min_duration_min: task.min_duration_min, max_duration_min: task.max_duration_min };
        const prevSchedule = schedule;
        schedule = schedule.map(day => {
            if (day.date === sourceDate) return { ...day, tasks: day.tasks.filter(t => t.id !== taskId) };
            if (day.date === targetDate) return { ...day, tasks: [...day.tasks, scheduleTask] };
            return day;
        });

        const res = await api(`${config.organizerTasksEndpoint}/${taskId}`, 'PUT', { pinned_dates });
        if (res?.success) {
            tasks = tasks.map(t => t.id === taskId ? res.task : t);
            weekDirty = true;
            toast.success(`"${task.title}" moved to ${targetDate}`);
        } else {
            schedule = prevSchedule;
            toast.error('Failed to move task');
        }
    }

    async function recomputeSchedule() {
        await refreshSchedule();
        weekDirty = false;
    }

    async function stopTask() {
        if (!activeSession) return;
        const res = await api(`${config.organizerTasksEndpoint}/${activeSession.task_id}/stop`, 'POST');
        if (res?.success) {
            activeSessionStore.set({ session: null, task: null, timerMin: null });
            localStorage.removeItem('activeTimerMin');
            tasks = tasks.map(t => t.id === res.task?.id ? res.task : t);
            toast.success('Session saved!');
            loadTodayMinutes();
            if (historyData) loadHistory();
        }
    }

    async function completeTask(task) {
        completingId = task.id;
        const res = await api(`${config.organizerTasksEndpoint}/${task.id}/complete`, 'POST');
        completingId = null;
        if (res?.success) {
            if (activeSession?.task_id === task.id) {
                activeSessionStore.set({ session: null, task: null, timerMin: null });
                localStorage.removeItem('activeTimerMin');
            }
            if (res.task?.is_active) {
                tasks = tasks.map(t => t.id === res.task.id ? res.task : t);
            } else {
                tasks = tasks.filter(t => t.id !== res.task?.id);
            }
            await refreshSchedule();
            loadTodayMinutes();
            toast.success(`${task.title} marked complete!`);
        }
    }

    async function refreshSchedule() {
        const res = await api(config.organizerScheduleEndpoint + `?days=7&tz_offset=${new Date().getTimezoneOffset()}`);
        if (res?.success) { schedule = res.schedule; overloadWarning = res.overload_warning; }
        const cap = await api(config.organizerCapacityEndpoint);
        if (cap?.success) atCapacity = cap.at_capacity;
    }

    async function saveTask(e) {
        const data = e.detail;
        const isEdit = !!editingTask;
        let res;
        if (isEdit) {
            res = await api(`${config.organizerTasksEndpoint}/${editingTask.id}`, 'PUT', data);
        } else {
            res = await api(config.organizerTasksEndpoint, 'POST', data);
        }
        if (res?.success) {
            tasks = isEdit
                ? tasks.map(t => t.id === res.task.id ? res.task : t)
                : [...tasks, res.task];
            taskModalOpen = false;
            editingTask = null;
            await refreshSchedule();
            toast.success(isEdit ? 'Task updated' : 'Task created');
        } else {
            toast.error('Failed to save task');
        }
    }

    async function deleteTask(task) {
        if (!confirm(`Delete "${task.title}"?`)) return;
        const res = await api(`${config.organizerTasksEndpoint}/${task.id}`, 'DELETE');
        if (res?.success) {
            tasks = tasks.filter(t => t.id !== task.id);
            await refreshSchedule();
            toast.success('Task deleted');
        }
    }

    async function addSection(e) {
        const res = await api(config.organizerSectionsEndpoint, 'POST', e.detail);
        if (res?.success) sections = res.sections;
    }

    async function deleteSection(e) {
        const s = e.detail;
        const res = await api(`${config.organizerSectionsEndpoint}/${s.id}`, 'DELETE');
        if (res?.success) sections = res.sections;
    }

    async function loadStats() {
        statsLoading = true;
        const res = await api(config.organizerStatsEndpoint);
        if (res?.success) statsData = res;
        statsLoading = false;
    }

    async function loadHistory() {
        historyLoading = true;
        historyData = null;
        const res = await api(`${config.organizerHistoryEndpoint}?week_start=${historyWeekStart}`);
        if (res?.success) historyData = res;
        historyLoading = false;
    }

    function changeWeek(delta) {
        const d = new Date(historyWeekStart + 'T12:00:00');
        d.setDate(d.getDate() + delta * 7);
        historyWeekStart = d.toISOString().slice(0, 10);
        loadHistory();
    }

    $: historyDays = historyData ? Array.from({ length: 7 }, (_, i) => {
        const d = new Date(historyData.week_start + 'T12:00:00');
        d.setDate(d.getDate() + i);
        const pad = n => String(n).padStart(2, '0');
        const dateStr = `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;
        return {
            dateStr,
            dayName: d.toLocaleDateString('en', { weekday: 'long' }),
            isToday: dateStr === new Date().toLocaleDateString('en-CA'),
        };
    }) : [];

    async function updateSession(e) {
        const { sessionId, startTime, endTime } = e.detail;
        const res = await api(`/organizer/sessions/${sessionId}`, 'PUT', { start_time: startTime, end_time: endTime });
        if (res?.success) {
            historyData = {
                ...historyData,
                sessions: historyData.sessions.map(s => s.id === sessionId ? {
                    ...s,
                    start_time: res.session.start_time,
                    end_time: res.session.end_time,
                    duration_min: Math.round(res.session.duration_min ?? 0),
                } : s),
            };
            toast.success('Session updated');
            refreshSchedule();
        } else {
            toast.error('Failed to update session');
        }
    }

    async function createSession(e) {
        const { taskId, startTime, endTime } = e.detail;
        const res = await api('/organizer/sessions', 'POST', { task_id: taskId, start_time: startTime, end_time: endTime });
        if (res?.success) {
            historyData = { ...historyData, sessions: [...historyData.sessions, res.session] };
            toast.success('Session logged');
            refreshSchedule();
        } else {
            toast.error('Failed to log session');
        }
    }

    async function deleteSession(e) {
        const { sessionId } = e.detail;
        const res = await api(`/organizer/sessions/${sessionId}`, 'DELETE');
        if (res?.success) {
            historyData = { ...historyData, sessions: historyData.sessions.filter(s => s.id !== sessionId) };
            toast.success('Session deleted');
            refreshSchedule();
        } else {
            toast.error('Failed to delete session');
        }
    }

    async function reorderSections(e) {
        const res = await api(`${config.organizerSectionsEndpoint}/reorder`, 'PUT', { section_ids: e.detail });
        if (res?.success) sections = res.sections;
    }

    function openSectionEdit(e) {
        editingSection = e.detail;
        sectionEditOpen = true;
    }

    async function saveSection(e) {
        const s = e.detail;
        const res = await api(`${config.organizerSectionsEndpoint}/${s.id}`, 'PUT', { name: s.name, day_configs: s.day_configs });
        if (res?.success) sections = res.sections;
        sectionEditOpen = false;
        editingSection = null;
    }

    const URGENCY_RANK  = { overdue: 0, time_to_do: 1, needs_doing: 2, upcoming: 3 };
    const PRIORITY_RANK = { high: 0, medium: 1, low: 2 };
    const taskScore = (t) => (URGENCY_RANK[t.urgency] ?? 4) * 2 + (PRIORITY_RANK[t.priority] ?? 1);

    const SECTION_PALETTE = [
        { border: 'border-indigo-700/50', bg: 'bg-indigo-900/10', label: 'text-indigo-400', leftBorder: 'border-indigo-500' },
        { border: 'border-violet-700/50', bg: 'bg-violet-900/10', label: 'text-violet-400', leftBorder: 'border-violet-500' },
        { border: 'border-cyan-700/50',   bg: 'bg-cyan-900/10',   label: 'text-cyan-400',   leftBorder: 'border-cyan-500'   },
        { border: 'border-teal-700/50',   bg: 'bg-teal-900/10',   label: 'text-teal-400',   leftBorder: 'border-teal-500'   },
        { border: 'border-amber-700/50',  bg: 'bg-amber-900/10',  label: 'text-amber-400',  leftBorder: 'border-amber-500'  },
        { border: 'border-rose-700/50',   bg: 'bg-rose-900/10',   label: 'text-rose-400',   leftBorder: 'border-rose-500'   },
    ];

    function paletteFor(sectionId) {
        const idx = sections.findIndex(s => s.id === sectionId);
        return SECTION_PALETTE[Math.max(0, idx) % SECTION_PALETTE.length];
    }

    function groupBySection(taskList) {
        const map = new Map();
        for (const t of taskList) {
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

    $: sortedTasks = [...tasks].sort((a, b) => taskScore(a) - taskScore(b));

    $: filteredTasks = selectedSectionId === null
        ? sortedTasks
        : sortedTasks.filter(t => t.section_id === selectedSectionId);

    $: todayTasks = schedule[0]?.tasks ?? [];
    $: todaySectionGroups = groupBySection(todayTasks);

    const TAB_GROUPS = [
        [
            { id: 'today',     label: 'Today'      },
            { id: 'week',      label: 'This Week'  },
        ],
        [
            { id: 'tasks',     label: 'All Tasks'  },
            { id: 'deepwork',  label: 'Fixed'      },
            { id: 'recurring', label: 'Recurring'  },
            { id: 'oneoff',    label: 'One-off'    },
        ],
        [
            { id: 'history',   label: 'History'    },
            { id: 'stats',     label: 'Stats'      },
        ],
    ];

    $: recurringTasks = tasks.filter(t => !t.is_one_off && (t.schedule_type || 'recurring') === 'recurring');
    $: oneOffTasks = tasks.filter(t => t.is_one_off);
    $: deepWorkTasks = tasks.filter(t => t.schedule_type === 'deep_work');
    $: filteredRecurring = selectedSectionId === null ? recurringTasks : recurringTasks.filter(t => t.section_id === selectedSectionId);
    $: filteredOneOff = selectedSectionId === null ? oneOffTasks : oneOffTasks.filter(t => t.section_id === selectedSectionId);
    $: filteredDeepWork = selectedSectionId === null ? deepWorkTasks : deepWorkTasks.filter(t => t.section_id === selectedSectionId);
</script>

<div class="max-w-5xl mx-auto px-4 py-6 space-y-4">

    {#if overloadWarning}
        <div class="flex items-start gap-2 px-4 py-2.5 bg-red-900/30 border border-red-700/50 rounded-lg text-sm text-red-300">
            <svg xmlns="http://www.w3.org/2000/svg" class="size-4 mt-0.5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
            <span>Schedule overload detected — some tasks cannot fit in available work hours this week.</span>
        </div>
    {/if}

    {#if atCapacity}
        <div class="flex items-start gap-2 px-4 py-2.5 bg-amber-900/30 border border-amber-700/50 rounded-lg text-sm text-amber-300">
            <svg xmlns="http://www.w3.org/2000/svg" class="size-4 mt-0.5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            <span>You are at or near capacity. Adding more tasks may push existing ones past their recurrence window.</span>
        </div>
    {/if}

    <div class="grid grid-cols-3 items-stretch border-b border-slate-700">
        {#each TAB_GROUPS as group, gi}
            <div class="flex gap-1 shrink-0 {gi === 1 ? 'justify-center' : gi === 2 ? 'justify-end' : ''}">
                {#each group as t}
                    <button
                        on:click={() => { tab = t.id; if (t.id === 'history' && !historyData) loadHistory(); if (t.id === 'stats' && !statsData) loadStats(); }}
                        class="px-4 py-2 text-sm font-medium whitespace-nowrap transition-colors {tab === t.id ? 'text-indigo-400 border-b-2 border-indigo-500 -mb-px' : 'text-slate-400 hover:text-slate-200'}">
                        {t.label}
                    </button>
                {/each}
            </div>
        {/each}
    </div>

    {#if loading}
        <div class="flex justify-center py-12">
            <div class="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
        </div>

    {:else if tab === 'today'}
        <div class="space-y-3">
            <div class="flex items-center justify-between">
                <h2 class="text-sm font-semibold text-slate-300">
                    {schedule[0]?.day_name ?? ''} · {schedule[0]?.date ?? ''}
                </h2>
                <div class="flex gap-2">
                    <button
                        on:click={() => assignDayOpen = true}
                        class="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-slate-700 hover:bg-slate-600 text-slate-200 rounded font-semibold transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
                        </svg>
                        Assign to Day
                    </button>
                    <button
                        on:click={() => quickAddOpen = true}
                        class="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-rose-700 hover:bg-rose-600 text-white rounded font-semibold transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
                        </svg>
                        Create Urgent Task
                    </button>
                </div>
            </div>

            {#if todayTasks.length === 0}
                <div class="py-8 text-center text-slate-500 text-sm">
                    {schedule[0]?.is_work_day ? 'Nothing scheduled for today — all caught up!' : 'Rest day. Enjoy the break.'}
                </div>
            {:else}
                <div class="space-y-3">
                    {#each todaySectionGroups as group}
                        <div class="rounded-lg border {group.section ? group.palette.border + ' ' + group.palette.bg : 'border-slate-700/40'} p-2.5">
                            {#if group.section}
                                <div class="text-xs font-semibold {group.palette.label} mb-2">{group.section.name}</div>
                            {/if}
                            <div class="grid gap-1.5 sm:grid-cols-2">
                                {#each group.tasks as t}
                                    {@const fullTask = tasks.find(tk => tk.id === t.id)}
                                    {#if fullTask}
                                        <TaskCard
                                            task={fullTask}
                                            {sections}
                                            compact
                                            skippable
                                            activeSessionTaskId={activeSession?.task_id}
                                            {completingId}
                                            todayMin={taskTodayMin[fullTask.id] ?? 0}
                                            on:start={(e) => startTask(e.detail)}
                                            on:stop={stopTask}
                                            on:complete={(e) => completeTask(e.detail)}
                                            on:skip={(e) => skipTask(e.detail)}
                                            on:edit={(e) => { editingTask = e.detail; taskModalOpen = true; }}
                                            on:delete={(e) => deleteTask(e.detail)} />
                                    {/if}
                                {/each}
                            </div>
                        </div>
                    {/each}
                </div>
            {/if}
        </div>

    {:else if tab === 'week'}
        <div class="space-y-3">
            <div class="flex items-center justify-between">
                <h2 class="text-sm font-semibold text-slate-300">7-Day Schedule</h2>
                <button
                    on:click={() => assignDayOpen = true}
                    class="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-slate-700 hover:bg-slate-600 text-slate-200 rounded font-semibold transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
                    </svg>
                    Assign to Day
                </button>
            </div>
            {#if weekDirty}
                <div class="flex justify-center">
                    <button
                        on:click={recomputeSchedule}
                        class="flex items-center gap-2 px-4 py-2 text-sm font-semibold bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg shadow-lg transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="size-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
                        </svg>
                        Recompute Schedule
                    </button>
                </div>
            {/if}
            <ScheduleGrid {schedule} {sections} on:assign={assignFromWeekGrid} on:edit={(e) => { editingTask = tasks.find(t => t.id === e.detail) ?? null; taskModalOpen = true; }} />
        </div>

    {:else if tab === 'tasks' || tab === 'recurring' || tab === 'oneoff' || tab === 'deepwork'}
        {@const tabTasks = tab === 'tasks' ? filteredTasks : tab === 'recurring' ? filteredRecurring : tab === 'oneoff' ? filteredOneOff : filteredDeepWork}
        <div class="flex gap-4">
            <div class="w-44 shrink-0 border-r border-slate-700 pr-3">
                <SectionsSidebar
                    {sections}
                    selectedId={selectedSectionId}
                    on:select={(e) => selectedSectionId = e.detail}
                    on:add={addSection}
                    on:editRequest={openSectionEdit}
                    on:delete={deleteSection}
                    on:reorder={reorderSections} />
            </div>

            <div class="flex-1 min-w-0 space-y-3">
                <div class="flex items-center justify-between">
                    <h2 class="text-sm font-semibold text-slate-300">{tabTasks.length} task{tabTasks.length !== 1 ? 's' : ''}</h2>
                    {#if tab === 'oneoff'}
                        <button
                            on:click={() => quickAddOpen = true}
                            class="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-rose-700 hover:bg-rose-600 text-white rounded font-semibold transition-colors">
                            <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
                            </svg>
                            Add One-off
                        </button>
                    {:else if tab === 'deepwork'}
                        <button
                            on:click={() => { editingTask = null; taskModalOpen = true; }}
                            class="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-emerald-700 hover:bg-emerald-600 text-white rounded font-semibold transition-colors">
                            <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
                            </svg>
                            New Fixed Task
                        </button>
                    {:else}
                        <button
                            on:click={() => { editingTask = null; taskModalOpen = true; }}
                            class="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-indigo-600 hover:bg-indigo-500 text-white rounded font-semibold transition-colors">
                            <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
                            </svg>
                            {tab === 'recurring' ? 'New Recurring' : 'New Task'}
                        </button>
                    {/if}
                </div>

                {#if tabTasks.length === 0}
                    <div class="py-12 text-center space-y-3">
                        <p class="text-slate-500 text-sm">{tab === 'tasks' && tasks.length === 0 ? 'No tasks yet.' : 'No tasks in this section.'}</p>
                        {#if tab === 'tasks' && tasks.length === 0}
                            <button
                                on:click={() => { editingTask = null; taskModalOpen = true; }}
                                class="px-4 py-2 text-sm bg-indigo-600 hover:bg-indigo-500 text-white rounded font-semibold transition-colors">
                                Add your first task
                            </button>
                        {/if}
                    </div>
                {:else}
                    <div class="grid gap-2 sm:grid-cols-2">
                        {#each tabTasks as task}
                            <TaskCard
                                {task}
                                {sections}
                                activeSessionTaskId={activeSession?.task_id}
                                {completingId}
                                on:start={(e) => startTask(e.detail)}
                                on:stop={stopTask}
                                on:complete={(e) => completeTask(e.detail)}
                                on:edit={(e) => { editingTask = e.detail; taskModalOpen = true; }}
                                on:delete={(e) => deleteTask(e.detail)} />
                        {/each}
                    </div>
                {/if}
            </div>
        </div>

    {:else if tab === 'history'}
        <div class="flex flex-col" style="height: calc(100vh - 13rem);">
            <div class="flex items-center justify-between mb-3 shrink-0">
                <h2 class="text-sm font-semibold text-slate-300">Work History</h2>
                <div class="flex items-center gap-2">
                    <button on:click={() => changeWeek(-1)} class="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="size-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="15 18 9 12 15 6"/>
                        </svg>
                    </button>
                    <span class="text-xs text-slate-400 w-32 text-center">
                        {historyData ? `${historyData.week_start} – ${historyDays[6]?.dateStr ?? ''}` : ''}
                    </span>
                    <button on:click={() => changeWeek(1)} class="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="size-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="9 18 15 12 9 6"/>
                        </svg>
                    </button>
                </div>
            </div>

            {#if historyLoading}
                <div class="flex-1 flex items-center justify-center">
                    <div class="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
                </div>
            {:else if historyData}
                <div class="flex-1 min-h-0">
                    <HistoryCalendar
                        sessions={historyData.sessions}
                        timeBlocks={historyData.time_blocks}
                        sections={historyData.sections}
                        {tasks}
                        days={historyDays}
                        on:updatesession={updateSession}
                        on:deletesession={deleteSession}
                        on:createsession={createSession} />
                </div>
            {/if}
        </div>

    {:else if tab === 'stats'}
        {#if statsLoading}
            <div class="flex justify-center py-12">
                <div class="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
        {:else if statsData}
            <StatsPanel stats={statsData} {sections} />
        {/if}
    {/if}
</div>

<TaskModal
    open={taskModalOpen}
    task={editingTask}
    presetScheduleType={editingTask ? null : (tab === 'deepwork' ? 'deep_work' : null)}
    {sections}
    on:save={saveTask}
    on:close={() => { taskModalOpen = false; editingTask = null; }} />


<SectionEditModal
    open={sectionEditOpen}
    section={editingSection}
    on:save={saveSection}
    on:close={() => { sectionEditOpen = false; editingSection = null; }} />

<QuickAddModal
    open={quickAddOpen}
    {sections}
    defaultOneOff={tab === 'oneoff' || tab === 'today'}
    on:save={quickAddTask}
    on:close={() => quickAddOpen = false} />

<AssignDayModal
    open={assignDayOpen}
    {tasks}
    {sections}
    {schedule}
    on:assign={assignTaskToDay}
    on:close={() => assignDayOpen = false} />
