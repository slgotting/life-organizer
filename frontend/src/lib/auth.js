import config, { buildServerEndpoint } from '../config/config';
import { authStore } from '../stores/auth';
import { handleApiResponse } from './api';
import { objectToFormData } from '../components/slg/lib/requests';
import toast from "svelte-french-toast";
import { goto } from "$app/navigation";

export const handleLogin = async (email, password, failureCallback) => {
    try {
        const formData = new FormData();
        formData.append('email', email);
        formData.append('password', password);

        const response = await fetch(buildServerEndpoint(config.loginEndpoint), {
            method: 'POST',
            body: formData
        });

        const json = await response.json();
        if (response.ok) {
            authStore.update((store) => {
                store.isAuthenticated = true;
                store.user = json.user;
                store.token = json.jwt;
                return store;
            });
            return true;
        } else {
            failureCallback(json.error);
        }
    } catch (error) { /* empty */ }
};

// const handleSignup = async (email, password, confirmPassword, failureCallback) => {
export const handleSignup = async (email, password, confirmPassword, failureCallback) => {
    try {
        const formData = new FormData();
        formData.append('email', email);
        formData.append('password', password);
        formData.append('confirm-password', confirmPassword);

        const response = await fetch(buildServerEndpoint(config.signUpEndpoint), {
            method: 'POST',
            body: formData
        });

        const json = await response.json();
        if (response.ok) {
            authStore.update((store) => {
                store.isAuthenticated = true;
                store.user = json.user;
                store.token = json.jwt;
                return store;
            });
            return true;
        } else {
            failureCallback(json.error);
        }
    } catch (error) { /* empty */ }
};

export const handleForgotPassword = async (email, failureCallback) => {
    try {
        const formData = new FormData();
        formData.append('email', email);

        const response = await fetch(buildServerEndpoint(config.forgotPasswordEndpoint), {
            method: 'POST',
            body: formData
        });

        const json = await response.json();
        if (response.ok) {
            return true;
        } else {
            failureCallback(json.error);
        }
    } catch (error) {
    }
}

export const handleResetPassword = async (token, password, failureCallback) => {
    try {
        const formData = new FormData();
        formData.append('password', password);

        const response = await fetch(buildServerEndpoint(config.resetPasswordEndpoint) + `/${token}`, {
            method: 'POST',
            body: formData
        });

        const json = await response.json();
        if (response.ok) {
            return true;
        } else {
            failureCallback(json.error);
        }
    } catch (error) {
    }
}

export const handleDeleteAccount = async (email, token, failureCallback) => {
    try {
        const formData = new FormData();
        formData.append('email', email);

        const response = await authenticatedFormRequest(
            buildServerEndpoint(config.deleteAccountEndpoint),
            "DELETE",
            token,
            formData
        )

        const json = await response.json();
        if (response.ok) {
            toast.success(json.success, {duration: 5000});
            logoutUser(() => goto('/'));
        } else {
            failureCallback(json.error);
        }
    } catch (error) {
    }
}

export const logoutUser = (callback) => {
    authStore.update((store) => {
        store.isAuthenticated = false;
        store.user = null;
        store.token = null;
        return store;
    });
    callback();
};

export const authenticatedPostRequest = (url, token) => {
    return fetch(url, {
        method: "POST",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}

export const authenticatedGetRequest = (url, token) => {
    return fetch(url, {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
}

export const authenticatedFormRequest = async (url, method, token, data) => {
    const formData = (data instanceof FormData) ? data : objectToFormData(data);

    return await fetch(url, {
        method: method,
        headers: {
            Authorization: `Bearer ${token}`,
        },
        body: formData,
    });
};

export const authenticatedJSONRequest = async (url, method, token, data) => {
    return await fetch(url, {
        method: method,
        headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
}