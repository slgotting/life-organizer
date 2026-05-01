<script>
    import { authStore } from "../../stores/auth";
    import { handleSignup } from "../../lib/auth";
    import { goto } from "$app/navigation";
    import { changePlan } from "../../components/Subscription/subscription";
    import Loader from "../../components/slg/loaders/Loader.svelte";
    import toast from "svelte-french-toast";

    const isAuthenticated = $authStore.isAuthenticated;

    if (isAuthenticated) {
        goto("/");
    }

    let email = "";
    let password = "";
    let confirmPassword = "";
    let errorMessage = "";

    let stripePortalLoading = false
    let signUpLoading = false

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (password !== confirmPassword) {
            errorMessage = "Passwords need to match";
        } else if (password.length < 8) {
            errorMessage = "Password not strong enough";
        } else {
            signUpLoading = true;
            const result = await handleSignup(email, password, confirmPassword, (errorString) => (errorMessage = errorString));

            const urlParams = new URLSearchParams(window.location.search);
            const planPurchase = urlParams.get('plan');

            if (result) {
                if (planPurchase) {
                    buyPlan(planPurchase);
                } else {
                    goto('/');
                }
            }
        }
    };

    async function buyPlan(type) {
        try {
            stripePortalLoading = true;
            const data = await changePlan(type, "Credit Card");
            stripePortalLoading = false;
            if (data.url) {
                window.location = data.url;
            }
            if (data.success) {
                toast.success(data.success, {duration:6000});
            } else if (data.error) {
                toast.error(data.error, {duration:6000});
            }
        } catch {
            stripePortalLoading = false;
            toast.error("Unknown error", {duration:6000});
        }
    }
</script>

<div class="flex min-h-full flex-1 flex-col px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <img class="mx-auto h-10 w-auto" src="/icon-only.png" alt="%%APP_NAME%%" />
        <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-daw-gray-900">Create a new account</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form on:submit={handleSubmit} class="space-y-6">
            <div>
                <label for="email" class="block text-sm font-medium leading-6 text-daw-gray-900"> Email address </label>
                <div class="mt-2">
                    <input
                        bind:value={email}
                        type="email"
                        id="email"
                        name="email"
                        autocomplete="email"
                        required
                        class="block w-full rounded-md border-0 py-1.5 indent-0 bg-white dark:bg-gray-700 text-daw-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-daw-gray-400 focus:ring-2 focus:ring-inset focus:ring-daw-blue-600 sm:text-sm sm:leading-6" />
                </div>
            </div>

            <div>
                <label for="password" class="block text-sm font-medium leading-6 text-daw-gray-900"> Password </label>
                <div class="mt-2">
                    <input
                        bind:value={password}
                        type="password"
                        id="password"
                        name="password"
                        autocomplete="new-password"
                        required
                        class="block w-full rounded-md border-0 py-1.5 indent-0 bg-white dark:bg-gray-700 text-daw-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-daw-gray-400 focus:ring-2 focus:ring-inset focus:ring-daw-blue-600 sm:text-xl sm:leading-6" />
                </div>
            </div>

            <div>
                <label for="confirm-password" class="block text-sm font-medium leading-6 text-daw-gray-900"> Confirm Password </label>
                <div class="mt-2">
                    <input
                        bind:value={confirmPassword}
                        type="password"
                        id="confirm-password"
                        name="confirm-password"
                        autocomplete="new-password"
                        required
                        class="block w-full rounded-md border-0 py-1.5 indent-0 bg-white dark:bg-gray-700 text-daw-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-daw-gray-400 focus:ring-2 focus:ring-inset focus:ring-daw-blue-600 sm:text-xl sm:leading-6" />
                </div>
            </div>

            {#if errorMessage}
                <div class="text-daw-red-500 text-sm">
                    {errorMessage}
                </div>
            {/if}

            <div>
                <button
                    type="submit"
                    class="flex w-full justify-center items-center rounded-md bg-daw-blue-500 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-daw-blue-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                    {#if stripePortalLoading}
                    <span>Redirecting... </span>
                    <Loader />
                    {:else if signUpLoading}
                    <Loader />
                    {:else}
                    Sign up
                    {/if}
                </button>
            </div>
        </form>

        <p class="mt-10 text-center text-sm text-daw-gray-500">
            Already have an account?{" "}
            <a href="/signin" class="font-semibold leading-6 text-daw-blue-600 hover:text-daw-blue-500">Sign in</a>
        </p>
    </div>
</div>
