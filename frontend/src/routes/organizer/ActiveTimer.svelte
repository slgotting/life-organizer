<script>
    import { createEventDispatcher, onMount, onDestroy } from 'svelte';
    import { Capacitor } from '@capacitor/core';
    import { KeepAwake } from '@capacitor-community/keep-awake';
    export let session;
    export let task;
    export let initialTargetMin = null;

    const dispatch = createEventDispatcher();

    let elapsedSec = 0;
    let interval;
    let targetSec = initialTargetMin ? initialTargetMin * 60 : null;
    let alarmActive = false;
    let silenced = false;
    let beepInterval;
    let audioCtx;
    let wakeLock = null;

    async function requestWakeLock() {
        if (!('wakeLock' in navigator)) return;
        try {
            wakeLock = await navigator.wakeLock.request('screen');
            wakeLock.addEventListener('release', () => { wakeLock = null; });
        } catch (_) {}
    }

    function onVisibilityChange() {
        if (document.visibilityState === 'visible') requestWakeLock();
    }

    onMount(async () => {
        if (Capacitor.isNativePlatform()) {
            try { await KeepAwake.keepAwake(); } catch (_) {}
        } else {
            requestWakeLock();
            document.addEventListener('visibilitychange', onVisibilityChange);
        }
    });

    function beep() {
        try {
            audioCtx = audioCtx || new (window.AudioContext || window.webkitAudioContext)();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.frequency.value = 880;
            gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.4);
            osc.start(audioCtx.currentTime);
            osc.stop(audioCtx.currentTime + 0.4);
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
        if (Capacitor.isNativePlatform()) {
            try { KeepAwake.allowSleep(); } catch (_) {}
        } else {
            wakeLock?.release();
            document.removeEventListener('visibilitychange', onVisibilityChange);
        }
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
