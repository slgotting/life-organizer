import { writable } from 'svelte/store';
export const pulseDataStore = writable({ tasks: [], sections: [] });
