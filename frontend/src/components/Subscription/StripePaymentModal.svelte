<!-- @format -->
<script>
    import Modal from "../slg/modals/BaseModal.svelte";
    import Loader from "../slg/loaders/Loader.svelte";

    import { loadStripe } from "@stripe/stripe-js";
    import { Elements, PaymentElement, EmbeddedCheckout } from "svelte-stripe";
    import { onMount } from "svelte";
    import config from "../../config/config";
    import toast from "svelte-french-toast";

    let stripe;
    let elements;
    let loading;
    let error;

    export let open = false;
    export let subscriptionId;
    export let clientSecret;

    let processing = false;

    async function submit() {
        // avoid processing duplicates
        if (processing) return;

        processing = true;

        // confirm payment with stripe
        const result = await stripe.confirmPayment({
            elements,
            redirect: "if_required",
        });

        if (result.error) {
            // payment failed, notify user
            error = result.error;
            processing = false;
            toast.error("There was an issue handling your request. We are looking into the issue and appreciate your patience.", {duration: 5000})
        } else {
            // payment succeeeded; show thanks
            toast.success("🎉 Thank you for subscribing!", {duration: 3000})
            open = false;
        }
    }

    onMount(async () => {
        loading = true;
        stripe = await loadStripe(config.publicStripeKey);
        loading = false;
    });
</script>

<Modal cssPosition={"absolute"} bind:open>
    <div class="relative w-96 min-h-96 flex flex-col items-center p-4 bg-white dark:bg-gray-700 text-white rounded-md shadow-md text-sm">
    {#if loading}
        <div class="w-8 mx-auto mt-8">
            <Loader />
        </div>
    {:else}
        <form on:submit|preventDefault={submit}>
            <EmbeddedCheckout
                {stripe}
                {clientSecret}
                bind:elements
            />
            <!-- <Elements
                {stripe}
                {clientSecret}
                bind:elements
            >
                <PaymentElement />
            </Elements> -->

            <button type="submit">Pay</button>
        </form>
    {/if}
    </div>
</Modal>
