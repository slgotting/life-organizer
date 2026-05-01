
import { writable } from 'svelte/store';

export const settingsModalOpenStore = writable(false);

// since we cannot use await here to initialize the settings,
//  you must set them in the component yourself
//      onMount(() => {
//          getSettingsLocal().then((settings_) => {
//              settings = settings_;
//          });
// do not set the onMount function to async, it breaks the unmount return function
export const settingsStore = writable({});
