<!-- @format -->
<script>
    import DeleteWithInput from "../../components/slg/confirmation/DeleteWithInput.svelte";
    import { handleDeleteAccount } from "../../lib/auth";
    import { onMount } from "svelte";
    import { getFromLocalStorage } from "../../components/slg/lib/localStorage";
    import Subscription from "../../components/Subscription/Subscription.svelte";
    import Button from "../../components/slg/primitives/Button.svelte";

    let deleteAccountModalOpen = false;
    let authData;
    let email;
    let deleteInputRequired;

    let errorMessage = "";

    onMount(() => {
        authData = getFromLocalStorage('auth')
        email = authData.user;
        deleteInputRequired = email;
    });

</script>

<div class="flex justify-center">
    <main class="max-w-screen-sm">
        <h1 class="sr-only">Account Settings</h1>

        <div class="divide-y divide-white/5 space-y-8">

            <Subscription />

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
