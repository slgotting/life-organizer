import { writable } from 'svelte/store';
export const activeSessionStore = writable({ session: null, task: null, timerMin: null });
