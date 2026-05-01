import { writable } from 'svelte/store';
import { getInitialState } from './localStorage'

const initialAuthState = {
    'isAuthenticated': false,
    'user': null,
    'token': null,
}

export const authStore = writable(getInitialState('auth', initialAuthState));

authStore.subscribe(($authStore) => {
    localStorage.setItem('auth', JSON.stringify($authStore));
});
