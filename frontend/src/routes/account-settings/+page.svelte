<!-- @format -->
<script>
    import DeleteWithInput from "../../components/slg/confirmation/DeleteWithInput.svelte";
    import { handleDeleteAccount } from "../../lib/auth";
    import { onMount } from "svelte";
    import { getFromLocalStorage } from "../../components/slg/lib/localStorage";
    import Button from "../../components/slg/primitives/Button.svelte";
    import { authenticatedJSONRequest } from "../../lib/auth";
    import { handleApiResponse } from "../../lib/api";
    import config, { buildServerEndpoint } from "../../config/config";

    let deleteAccountModalOpen = false;
    let authData;
    let email;
    let deleteInputRequired;

    let errorMessage = "";

    let pulsePrefs = { minGapMin: 30, gapMode: 'minimum' };

    function token() { return getFromLocalStorage('auth')?.token; }
    function api(endpoint, method = 'GET', data = undefined) {
        return authenticatedJSONRequest(buildServerEndpoint(endpoint), method, token(), data).then(handleApiResponse);
    }

    async function loadPulsePrefs() {
        const res = await api(config.organizerConfigEndpoint);
        if (res?.success) pulsePrefs = { minGapMin: res.pulse_min_gap_min ?? 30, gapMode: res.pulse_gap_mode ?? 'minimum' };
    }

    async function savePulsePrefs() {
        await api(config.organizerConfigEndpoint, 'PUT', { pulse_min_gap_min: pulsePrefs.minGapMin, pulse_gap_mode: pulsePrefs.gapMode });
    }

    onMount(() => {
        authData = getFromLocalStorage('auth')
        email = authData.user;
        deleteInputRequired = email;
        loadPulsePrefs();
    });

</script>

<div class="flex justify-center">
    <main class="max-w-screen-sm">
        <h1 class="sr-only">Account Settings</h1>

        <div class="divide-y divide-white/5 space-y-8">

            <div class="grid max-w-7xl grid-cols-1 gap-x-8 gap-y-10 px-4 py-16 sm:px-6 md:grid-cols-3 lg:px-8">
                <div>
                    <h2 class="text-base font-semibold leading-7 text-white">Pulse tasks</h2>
                    <p class="mt-1 text-sm leading-6 text-gray-400">
                        Controls how often pulse task reminders can appear, regardless of each task's individual interval.
                    </p>
                </div>
                <div class="md:col-span-2 space-y-6">
                    <div class="space-y-1.5">
                        <label class="block text-sm font-medium text-slate-300">Minimum gap between any pulse tasks (minutes)</label>
                        <p class="text-xs text-slate-500">After dismissing any pulse task, no other pulse task will appear for this many minutes.</p>
                        <input
                            type="number"
                            min="0"
                            step="1"
                            bind:value={pulsePrefs.minGapMin}
                            on:change={savePulsePrefs}
                            disabled={pulsePrefs.gapMode !== 'minimum'}
                            class="w-32 bg-slate-800 border border-slate-600 rounded px-3 py-1.5 text-sm text-slate-200 focus:outline-none focus:border-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed" />
                    </div>
                    <div class="space-y-2">
                        <label class="block text-sm font-medium text-slate-300">Timing preference</label>
                        <p class="text-xs text-slate-500">When a task uses Deterministic intervals, the global gap may cause the actual interval to drift from the target average. Choose which behaviour to prefer.</p>
                        <div class="flex gap-2">
                            {#each [{ value: 'minimum', label: 'Enforce minimum gap', desc: 'Global cooldown applies; deterministic tasks may drift.' }, { value: 'deterministic', label: 'Prefer deterministic', desc: 'No global gap; each task follows its own interval exactly.' }] as opt}
                                <button
                                    on:click={() => { pulsePrefs = { ...pulsePrefs, gapMode: opt.value }; savePulsePrefs(); }}
                                    class="flex-1 text-left px-3 py-2.5 rounded-lg border text-sm transition-colors {pulsePrefs.gapMode === opt.value ? 'border-indigo-500 bg-indigo-500/10 text-slate-100' : 'border-slate-600 bg-slate-800/50 text-slate-400 hover:border-slate-500'}">
                                    <div class="font-medium">{opt.label}</div>
                                    <div class="text-xs mt-0.5 {pulsePrefs.gapMode === opt.value ? 'text-slate-400' : 'text-slate-600'}">{opt.desc}</div>
                                </button>
                            {/each}
                        </div>
                    </div>
                </div>
            </div>

            <div class="grid max-w-7xl grid-cols-1 gap-x-8 gap-y-10 px-4 py-16 sm:px-6 md:grid-cols-3 lg:px-8">
                <div>
                    <h2 class="text-base font-semibold leading-7 text-white">Delete account</h2>
                    <p class="mt-1 text-sm leading-6 text-gray-400">
                        No longer want to use our service? You can delete your account here.
                    </p>
                </div>
                    <div>
                        <Button
                            on:click={() => {
                                deleteAccountModalOpen = true;
                            }}
                            classes={`w-36 button-base bg-red-500 hover:bg-red-400`}>
                            Delete
                        </Button>
                    </div>

                    {#if errorMessage}
                    <div class="text-red-500">
                        {errorMessage}
                    </div>
                    {/if}
            </div>
        </div>
    </main>
    <DeleteWithInput
        bind:open={deleteAccountModalOpen}
        deleteCallback={() => handleDeleteAccount(email, authData.token, (errorString) => errorMessage = errorString)}
        inputRequired={deleteInputRequired}
    >
        <div slot="title">Are you sure you want to?</div>
        <div slot="description">
            This action is not reversible. All information related to this
            account will be deleted permanently.
        </div>
        <div slot="deleteInput">
            Enter your email "<span class="italic text-red-600 font-bold text-lg">{deleteInputRequired}</span>" to confirm deletion
        </div>
    </DeleteWithInput>
</div>
