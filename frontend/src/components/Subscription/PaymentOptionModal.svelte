<!-- @format -->
<script>
    import { createEventDispatcher } from 'svelte';
    import Modal from "../slg/modals/BaseModal.svelte";
    import Button from "../slg/primitives/Button.svelte";
    import Loader from "../slg/loaders/Loader.svelte";
    import { changePlan } from "./subscription";

    const dispatch = createEventDispatcher();

    let loading;

    export let price = "$5.00";

    export let open = false;

    export let selectedPlanType;
    export let currentPlanType;

    export let options = ["Credit Card", "Solana"];
</script>

<Modal bind:open>
    <div class="relative w-96 flex flex-col items-center p-4 bg-white dark:bg-gray-700 text-white rounded-md shadow-md text-sm">
        {#if loading}
        <div class="w-8 mx-auto mt-8">
            <Loader />
        </div>
        {:else}
        <div class="flex items-center space-x-2">
            <div>
                {currentPlanType}
            </div>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25 21 12m0 0-3.75 3.75M21 12H3" />
            </svg>

            <div>
                {selectedPlanType}
            </div>
        </div>

        <div>
            {price}
        </div>

        <div class="mt-8 flex flex-col justify-center space-y-2">
            Pay with
            <Button on:click={async () => {
                loading = true;
                const data = await changePlan(selectedPlanType, "Credit Card");
                dispatch('openStripePayment', {
                    clientSecret: data.clientSecret,
                    subscriptionId: data.subscriptionId
                })
                open = false;
            }}
                classes={`button-base button-game`}
            >
                Credit Card
            </Button>
        </div>
        {/if}
    </div>
</Modal>
