<!-- @format -->
<script>
    import "../tailwind.css";
    import { authStore } from "../stores/auth";
    import { goto, afterNavigate, beforeNavigate } from "$app/navigation";
    import { page } from "$app/stores";
    import SettingsModal from "../components/SettingsModal.svelte";
    import toast, { Toaster } from "svelte-french-toast";
    import Footer from "../components/LandingPage/Footer.svelte";
    import { settingsModalOpenStore } from "../stores/settings";
    import { scheduleNotifications } from "../lib/notifications";
    import { onMount } from "svelte";
    import { authenticatedPostRequest, logoutUser, authenticatedJSONRequest } from "../lib/auth";
    import { handleApiResponse } from "../lib/api";
    import config, { buildServerEndpoint } from "../config/config";
    import { activeSessionStore } from "../stores/session";
    import ActiveTimer from "./organizer/ActiveTimer.svelte";

    const urlParams = new URLSearchParams(window.location.search);
    const toastParam = urlParams.get("toast");
    const TOAST_MAP = {
        // 'subscription-success-Basic': () => toast.success('Successfully subscribed to the Basic plan. Thank you for your support!', {duration: 4000}),
        // 'subscription-success-Cultivating': () => toast.success('Successfully subscribed to the Cultivating plan. Thank you for your support!', {duration: 4000}),
        // 'subscription-success-Learned': () => toast.success('Successfully subscribed to the Learned plan. Thank you for your support!', {duration: 4000}),
        "subscription-request-canceled": () => toast.error("Checkout was canceled.", { duration: 4000 }),
    };
    if (toastParam) {
        const toasts = toastParam.split(",");
        for (const t of toasts) {
            if (Object.keys(TOAST_MAP).includes(t)) {
                TOAST_MAP[t]();
            }
        }
    }

    let settingsModalOpen = false;

    settingsModalOpenStore.subscribe((bool) => {
        settingsModalOpen = bool;
    });

    const navItems = [{ loc: "/", name: "Home" }];

    $: isAuthenticated = $authStore.isAuthenticated;

    const nonAuthenticatedRoutes = [
        "/signin",
        "/signup",
        "/signout",
        "/forgot-password",
        "/reset-password",
        "/privacy-policy",
        "/roadmap",
        "/changelog",
        "/landing-page",
        "/how-it-works",
    ];

    afterNavigate(() => {
        let isOkRoute = false;
        if (!isAuthenticated) {
            const path = window.location.pathname;
            for (let route of nonAuthenticatedRoutes) {
                if (path === "/" || path.startsWith(route)) {
                    isOkRoute = true;
                }
            }
            if (isOkRoute) {
                return;
            } else {
                goto("/signin");
            }
        }
    });

    function layoutToken() {
        return JSON.parse(localStorage.getItem('auth'))?.token;
    }

    async function layoutApi(endpoint, method = 'GET', data = undefined) {
        const res = await authenticatedJSONRequest(buildServerEndpoint(endpoint), method, layoutToken(), data);
        return handleApiResponse(res);
    }

    async function layoutStopTask() {
        const session = $activeSessionStore.session;
        if (!session) return;
        const res = await layoutApi(`${config.organizerTasksEndpoint}/${session.task_id}/stop`, 'POST');
        if (res?.success) {
            activeSessionStore.set({ session: null, task: null, timerMin: null });
            localStorage.removeItem('activeTimerMin');
            toast.success('Session saved!');
        }
    }

    async function layoutCompleteTask() {
        const task = $activeSessionStore.task;
        if (!task) return;
        const res = await layoutApi(`${config.organizerTasksEndpoint}/${task.id}/complete`, 'POST');
        if (res?.success) {
            activeSessionStore.set({ session: null, task: null, timerMin: null });
            localStorage.removeItem('activeTimerMin');
            toast.success(`${task.title} marked complete!`);
        }
    }

    onMount(async () => {
        if ($authStore.isAuthenticated) {
            try {
                const res = await authenticatedPostRequest(
                    buildServerEndpoint(config.authorizeEndpoint),
                    $authStore.token
                );
                if (!res.ok) {
                    logoutUser(() => goto('/signin'));
                }
            } catch {
                // network error — don't force logout when offline
            }
            const sessRes = await layoutApi(config.organizerActiveSessionEndpoint);
            if (sessRes?.success && sessRes.session) {
                const stored = JSON.parse(localStorage.getItem('activeTimerMin') || 'null');
                const timerMin = stored?.sessionId === sessRes.session.id ? stored.timerMin : null;
                activeSessionStore.set({ session: sessRes.session, task: sessRes.task, timerMin });
            }
        } else {
            const path = window.location.pathname;
            const isOkRoute = path === '/' || nonAuthenticatedRoutes.some(r => path.startsWith(r));
            if (!isOkRoute) goto('/signin');
        }
    });
</script>
<svelte:head>
    <title>schedulr</title>
</svelte:head>

<nav class="fixed w-full flex items-center px-2 py-2 text-daw-blue-700 text-sm font-semibold border-b border-slate-600 bg-slate-900/30 z-30 backdrop-blur-sm">
    <div class="ml-4">
        <a href="/" class="flex space-x-2 items-center font-serif">
            <img class="w-8 h-8" src="/images/icon.svg" alt="schedulr Icon" />
        </a>
    </div>
    <div class="ml-auto mr-4 flex space-x-6">
        {#if $authStore.isAuthenticated}
            <a class="nav-base" href="/organizer" aria-current={$page.url.pathname.startsWith('/organizer')} title="Life Organizer">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                </svg>
            </a>
            <a class="nav-base" href="/how-it-works" aria-current={$page.url.pathname === '/how-it-works'} title="How it works">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />
                </svg>
            </a>
            <a class="nav-base" href={"/feedback"} aria-current={$page.url.pathname === "/feedback"} title="Give Feedback">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M8.625 9.75a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375m-13.5 3.01c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.184-4.183a1.14 1.14 0 0 1 .778-.332 48.294 48.294 0 0 0 5.83-.498c1.585-.233 2.708-1.626 2.708-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
                </svg>
            </a>
            <a class="nav-base" href={"/account-settings"} aria-current={$page.url.pathname === "/account-settings"} title="Account">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                </svg>
            </a>
            <a class="nav-base" href={"/signout"} aria-current={$page.url.pathname === "/signout"} title="Logout">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15m3 0 3-3m0 0-3-3m3 3H9" />
                </svg>
            </a>
        {:else}
            <a class="nav-base" href={"/signin"} aria-current={$page.url.pathname === "/signin"}>Login</a>
        {/if}
    </div>
</nav>

<main class="pt-16 sm:pt-24 w-full min-h-screen text-sm sm:text-lg">
    {#if $activeSessionStore.session && $activeSessionStore.task}
        <div class="sticky top-14 z-20 bg-slate-950/80 backdrop-blur-sm border-b border-slate-800/50">
            <div class="max-w-5xl mx-auto px-4 py-2">
                <ActiveTimer
                    session={$activeSessionStore.session}
                    task={$activeSessionStore.task}
                    initialTargetMin={$activeSessionStore.timerMin}
                    on:stop={layoutStopTask}
                    on:complete={layoutCompleteTask} />
            </div>
        </div>
    {/if}
    <svg aria-hidden="true" class="absolute inset-0 -z-10 h-full w-full stroke-white/10 [mask-image:radial-gradient(100%_100%_at_top_right,white,transparent)]">
        <defs>
            <pattern x="50%" y={-1} id="983e3e4c-de6d-4c3f-8d64-b9761d1534cc" width={200} height={200} patternUnits="userSpaceOnUse">
                <path d="M.5 200V.5H200" fill="none" />
            </pattern>
        </defs>
        <svg x="50%" y={-1} class="overflow-hidden fill-gray-800/20">
            <path d="M-200 0h201v201h-201Z M600 0h201v201h-201Z M-400 600h201v201h-201Z M200 800h201v201h-201Z" strokeWidth={0} />
        </svg>
        <rect fill="url(#983e3e4c-de6d-4c3f-8d64-b9761d1534cc)" width="100%" height="100%" strokeWidth={0} />
    </svg>
    <div aria-hidden="true" class="absolute left-0 top-10 -z-10 transform-gpu blur-3xl lg:top-[calc(50%-30rem)]">
        <div class="aspect-[1108/632] w-[100vw] bg-gradient-to-r from-[#4f7a99] to-[#3b35b1] opacity-20" />
    </div>
    <slot />

    <SettingsModal bind:isOpen={settingsModalOpen} />

    <Toaster containerClassName={"text-sm"} />
</main>

<Footer />
<style>
    main {
        padding-bottom: 1rem;
    }
</style>
