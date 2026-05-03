<!-- @format -->
<script>
    import { authStore } from "../../stores/auth";
    import { handleForgotPassword } from "../../lib/auth";
    import { goto } from "$app/navigation";
    import toast, { Toaster } from "svelte-french-toast";

    let email = "";
    let errorMessage = "";

    if ($authStore.isAuthenticated) {
        goto("/");
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        const result = await handleForgotPassword(email, (errorString) => (errorMessage = errorString));
        if (result) {
            toast.success("Password reset email sent.", {duration: 5000});
        }
    };
</script>

<div class="flex min-h-full flex-1 flex-col px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <img class="mx-auto h-10 w-auto" src="/icon-only.png" alt="schedulr" />
        <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-daw-gray-900">
            Forgot Your Password?
        </h2>
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

            {#if errorMessage}
                <div class="text-daw-red-500 text-sm">
                    {errorMessage}
                </div>
            {/if}

            <div>
                <button
                    type="submit"
                    class="flex w-full justify-center rounded-md bg-daw-blue-500 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-daw-blue-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                    Request Password Reset
                </button>
            </div>
        </form>

        <p class="mt-10 text-center text-sm text-daw-gray-500">
            Not a member?{" "}
            <a href="/signup" class="font-semibold leading-6 text-daw-blue-600 hover:text-daw-blue-500"> Sign up </a>
        </p>
    </div>
</div>
