<script>
    import { createEventDispatcher, onDestroy } from 'svelte';
    export let session;
    export let task;

    const dispatch = createEventDispatcher();

    let elapsedSec = 0;
    let interval;
    let targetSec = null;
    let alarmActive = false;
    let silenced = false;
    let beepInterval;
    let settingTimer = false;
    let timerInputMin = '';
    let audioCtx;

    function beep() {
        try {
            const ctx = audioCtx;
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.frequency.value = 880;
            gain.gain.setValueAtTime(0.3, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
            osc.start(ctx.currentTime);
            osc.stop(ctx.currentTime + 0.4);
        } catch (_) {}
    }

    function triggerAlarm() {
        alarmActive = true;
        beep();
        beepInterval = setInterval(beep, 5000);
    }

    function tick() {
        const start = new Date(session.start_time + 'Z');
        elapsedSec = Math.floor((Date.now() - start.getTime()) / 1000);
        if (targetSec !== null && !alarmActive && !silenced && elapsedSec >= targetSec) {
            triggerAlarm();
        }
    }

    $: if (session) {
        clearInterval(interval);
        tick();
        interval = setInterval(tick, 1000);
    }

    function setTimer() {
        const min = parseInt(timerInputMin);
        if (!min || min <= 0) return;
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        targetSec = min * 60;
        timerInputMin = '';
        settingTimer = false;
        if (elapsedSec >= targetSec) triggerAlarm();
    }

    function silence() {
        alarmActive = false;
        silenced = true;
        clearInterval(beepInterval);
    }

    function handleStop() {
        clearInterval(beepInterval);
        dispatch('stop');
    }

    function handleComplete() {
        clearInterval(beepInterval);
        dispatch('complete');
    }

    onDestroy(() => {
        clearInterval(interval);
        clearInterval(beepInterval);
    });

    function fmt(sec) {
        if (sec < 0) sec = 0;
        const h = Math.floor(sec / 3600);
        const m = Math.floor((sec % 3600) / 60);
        const s = sec % 60;
        const mm = String(m).padStart(2, '0');
        const ss = String(s).padStart(2, '0');
        return h > 0 ? `${h}:${mm}:${ss}` : `${mm}:${ss}`;
    }

    $: remaining = targetSec !== null ? targetSec - elapsedSec : null;
    $: overtime = remaining !== null && remaining < 0 ? -remaining : 0;
    $: timeDisplay = alarmActive ? `+${fmt(overtime)}` : remaining !== null ? fmt(Math.max(0, remaining)) : fmt(elapsedSec);
    $: timeColor = alarmActive ? 'text-amber-200' : (remaining !== null && remaining < 60) ? 'text-red-300' : (remaining !== null && remaining < 300) ? 'text-yellow-300' : 'text-emerald-200';
</script>

<div class="flex items-center gap-3 px-4 py-2 {alarmActive ? 'bg-amber-900/40 border-amber-700/50' : 'bg-emerald-900/40 border-emerald-700/50'} border rounded-lg transition-colors">
    <span class="relative flex h-2.5 w-2.5 shrink-0">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full {alarmActive ? 'bg-amber-400' : 'bg-emerald-400'} opacity-75"></span>
        <span class="relative inline-flex rounded-full h-2.5 w-2.5 {alarmActive ? 'bg-amber-500' : 'bg-emerald-500'}"></span>
    </span>

    <span class="{alarmActive ? 'text-amber-300' : 'text-emerald-300'} font-medium text-sm truncate min-w-0">{task?.title ?? 'Task'}</span>
    <span class="font-mono text-sm {timeColor} shrink-0">{timeDisplay}</span>

    {#if !alarmActive && !silenced && targetSec === null}
        {#if settingTimer}
            <div class="flex items-center gap-1 shrink-0">
                <input
                    type="number"
                    bind:value={timerInputMin}
                    min="1"
                    max="480"
                    placeholder="min"
                    on:keydown={(e) => e.key === 'Enter' && setTimer()}
                    class="w-14 text-center bg-slate-800 border border-slate-600 rounded px-2 py-0.5 text-xs text-slate-100 focus:outline-none focus:border-indigo-500" />
                <button on:click={setTimer} class="px-2 py-0.5 text-xs bg-indigo-700 hover:bg-indigo-600 text-white rounded transition-colors">Set</button>
                <button on:click={() => { settingTimer = false; timerInputMin = ''; }} class="text-slate-500 hover:text-slate-300 transition-colors leading-none">
                    <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                </button>
            </div>
        {:else}
            <button on:click={() => settingTimer = true} title="Set countdown timer" class="text-slate-500 hover:text-slate-300 transition-colors shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="size-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
                </svg>
            </button>
        {/if}
    {/if}

    <div class="ml-auto flex gap-2 shrink-0">
        {#if alarmActive}
            <button on:click={silence} class="px-3 py-1 text-xs font-semibold bg-amber-700 hover:bg-amber-600 text-white rounded transition-colors">
                Silence
            </button>
        {/if}
        <button on:click={handleStop} class="px-3 py-1 text-xs font-semibold bg-emerald-700 hover:bg-emerald-600 text-white rounded transition-colors">
            Stop
        </button>
        <button on:click={handleComplete} class="px-3 py-1 text-xs font-semibold bg-slate-600 hover:bg-slate-500 text-white rounded transition-colors">
            Mark Done
        </button>
    </div>
</div>
