import { authStore } from '../stores/auth';
import { goto } from '$app/navigation';

const INITIAL_AUTH = { isAuthenticated: false, user: null, token: null };

export const handleApiResponse = async (response) => {
    if (response.status === 401) {
        authStore.set(INITIAL_AUTH);
        goto('/signin');
        return null;
    }
    return response.json();
};