<!-- @format -->
<script>
    import { onMount } from "svelte";
    import { getSubscriptionDetails, changePlan, cancelPlan, purchaseLifetimeAccess, openStripeCustomerPortal } from "./subscription";
    import Modal from "../slg/modals/BaseModal.svelte";
    import DeleteConfirmation from "../slg/confirmation/Delete.svelte";
    import Loader from "../slg/loaders/Loader.svelte";
    import Button from "../slg/primitives/Button.svelte";
    import TrendingDownArrow from "../slg/images/TrendingDownArrow.svelte";
    import PaymentOptionModal from "./PaymentOptionModal.svelte";
    import StripePaymentModal from "./StripePaymentModal.svelte";
    import toast from "svelte-french-toast";
    import config, { buildServerEndpoint } from "../../config/config";
    import { authStore } from "../../stores/auth";

    import DescriptionWithArrowRight from "../slg/handdrawn/DescriptionWithArrowRight.svelte";
    import DescriptionWithArrowUp from "../slg/handdrawn/DescriptionWithArrowUp.svelte";
    import { authenticatedPostRequest } from "../../lib/auth";
    import Details from "./Details.svelte";
    import TrendingUpArrow from "../slg/images/TrendingUpArrow.svelte";

    let subscriptionDetails;
    let subscriptionDetailsLoading = true;

    let planTypes;
    let planTypesObject;
    let planTypeOrder;
    let paymentOptionModalOpen = false;
    let paymentPreviewModalOpen = false;
    let stripePortalLoading = false;
    let stripeCustomerPortalLoading = false;
    let purchaseLifetimeAccessLoading = false;
    let selectedPlanType;
    let currentPlanType;

    let stripePaymentModalOpen = false;
    let stripeClientSecret;
    let stripeSubscriptionId;

    let cancelPlanModalOpen = false;

    onMount(() => {
        getSubscriptionDetails().then((details) => {
            if (details && Object.keys(details).length > 0) {
                console.log(details);

                subscriptionDetails = details;
                currentPlanType = details.plan;
                planTypes = details.plan_types;
                planTypesObject = Object.fromEntries(planTypes.map((plan, idx) => [plan.plan, plan.access]));
                planTypeOrder = Object.fromEntries(planTypes.map((plan, idx) => [plan.plan, idx]));
                subscriptionDetailsLoading = false;
            } else {
                subscriptionDetailsLoading = "Failed to load";
            }
        });
    });
</script>

{#if !subscriptionDetailsLoading && subscriptionDetails}
    <div class="flex flex-col items-center justify">
        {#if !subscriptionDetails.lifetime_access}
        <div class="w-full mb-8 flex flex-col items-center justify-evenly">
            <div class="flex flex-col items-center max-w-48">
                <h1 class="mt-4 text-xl font-bold tracking-tight text-daw-gray-900 sm:text-2xl">Lifetime Access</h1>
                <div class="mt-1 text-sm text-daw-gray-600">Full access to all current and future features, forever.</div>
            </div>
            <Button
                loading={purchaseLifetimeAccessLoading}
                on:click={async () => {
                    purchaseLifetimeAccessLoading = true;
                    const data = await purchaseLifetimeAccess("Credit Card");
                    if (data.url) {
                        window.location = data.url;
                    }
                    if (data.success) {
                        toast.success(data.success, { duration: 6000 });
                    } else if (data.error) {
                        toast.error(data.error, { duration: 6000 });
                    }
                }}
                classes={`button-base button-primary mt-4`}>
                <span class="pr-3 border-r border-gray-300">$50</span>
                <span class="ml-3">Purchase</span>
            </Button>
        </div>
        {/if}

        <div class="w-full mb-8 flex flex-col md:flex-row justify-around items-center space-y-4">
            {#if !subscriptionDetails.lifetime_access}
                <div class="w-full flex justify-around items-center">
                    <Details
                        planName={""}
                        planAccess={subscriptionDetails.access}
                        autoUpdateWidth={true}
                        valueClass={"text-sm text-blue-500"}
                        keyClass={"text-sm"} />
                    <div class="flex flex-col items-center space-y-2">
                        <div class="">Plans</div>
                        {#each Object.keys(planTypesObject) as planType, i}
                            {#if planType != "Lifetime"}
                                <div class="relative w-full">
                                    {#if planType === subscriptionDetails.plan}
                                        <div class="absolute -left-8 -top-4">
                                            <DescriptionWithArrowRight size={"size-8"}>
                                                <div class="relative -left-12 top-8 text-gray-100 text-sm w-12" style="font-family: handwritten;">Current</div>
                                            </DescriptionWithArrowRight>
                                        </div>
                                    {/if}
                                    <Button
                                        disabled={planType === "Free"}
                                        on:click={async () => {
                                            if (planType == subscriptionDetails.plan) {
                                                toast.error(
                                                    "You are already on this plan and currently we are only using Stripe. Check back later to see if we've implemented Solana subscriptions!",
                                                    { duration: 6000 },
                                                );
                                                return;
                                            }
                                            selectedPlanType = planType;
                                            paymentPreviewModalOpen = true;
                                        }}
                                        classes={`button-game w-full
                                ${planType === subscriptionDetails.plan ? "current-plan" : ""}
                        `}>
                                        {planType}
                                    </Button>
                                </div>
                            {/if}
                        {/each}
                    </div>
                </div>
            {:else}
                <div class="w-full flex justify-around items-center">
                    <Details
                        planName={""}
                        planAccess={subscriptionDetails.access}
                        autoUpdateWidth={true}
                        valueClass={"text-sm text-blue-500"}
                        keyClass={"text-sm"} />
                    <div></div>
                    <div class="text-center flex flex-col justify-center items-center">
                        <h1 class="mt-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-3xl">Certified Sage</h1>
                        <p class="mt-2 text-base text-gray-500">Lifetime access to all features</p>
                    </div>
                </div>
            {/if}
        </div>
        {#if !subscriptionDetails.lifetime_access}
            <div class="w-full flex justify-evenly items-center">

                <div class="flex flex-col items-cener">
                    {#if !subscriptionDetails.canceled}
                        {#if !subscriptionDetails.plan === "Free"}
                        <div>
                            <Button
                                on:click={() => {
                                    cancelPlanModalOpen = true;
                                }}
                                classes={`button-base bg-red-500 hover:bg-red-400`}>
                                Cancel Subscription
                            </Button>
                        </div>
                        {/if}
                    {/if}
                    <div class="mt-2 flex text-sm">
                        {subscriptionDetails.canceled ? "Ends" : "Renews"}: {subscriptionDetails.renewal_date}
                    </div>
                </div>
                <div class="">
                <Button
                    loading={stripeCustomerPortalLoading}
                    on:click={async () => {
                        stripeCustomerPortalLoading = true;
                        const data = await openStripeCustomerPortal();
                        if (data.url) {
                            window.location = data.url;
                        } else {
                            toast.error(data.error, { duration: 6000 });
                        }
                    }}
                    classes={`button-game mt-4`}>
                    Open Billing Portal
                </Button>
                </div>
            </div>
        {/if}
    </div>
{:else if subscriptionDetailsLoading === "Failed to load"}
    <div class="flex justify-center items-center h-96 text-red-500">
        Failed to load
    </div>
{:else}
    <div class="flex justify-center items-center h-96">
        <div class="w-8 h-8">
            <Loader />
        </div>
    </div>
{/if}

<Modal bind:open={paymentPreviewModalOpen}>
    <div class="relative w-96 min-h-64 flex flex-col justify-center items-center p-4 bg-white dark:bg-gray-700 text-white rounded-md shadow-md text-md">
        <div class="flex flex-col justify-center items-center">
            <div class="font-bold">We partner with Stripe for simplified billing.</div>
            <div class="text-sm text-gray-400 tracking-tight">*%%APP_NAME%% is a subsidiary of Steezen, LLC</div>

            <div class="relative mt-8 flex items-center">
                <Details planName={currentPlanType} planAccess={planTypesObject[currentPlanType]} />
                {#if planTypeOrder[currentPlanType] > planTypeOrder[selectedPlanType]}
                    <TrendingDownArrow classes={"absolute top-0 left-1/2 -translate-x-1/2 size-8 text-red-500"} />
                {:else}
                    <TrendingUpArrow classes={"absolute top-0 left-1/2 -translate-x-1/2 size-8 text-green-500"} />
                {/if}
                <div class="ml-4">
                    <Details planName={selectedPlanType} planAccess={planTypesObject[selectedPlanType]} />
                </div>
            </div>
        </div>

        <div class="mt-16 mb-2 space-y-2">
            {#if currentPlanType === "Free"}
                <div class="flex space-x-2">
                    <div>${subscriptionDetails["plan_type_prices"][selectedPlanType].toFixed(2)}</div>
                    <div class="text-sm text-gray-500 self-end">/ month</div>
                </div>
            {:else if planTypeOrder[currentPlanType] > planTypeOrder[selectedPlanType]}
                <div class="flex space-x-2">
                    <div>$0.00</div>
                    <div class="text-sm text-gray-500 self-end">due now</div>
                </div>
                <div class="flex space-x-2">
                    <div>${subscriptionDetails["plan_type_prices"][selectedPlanType].toFixed(2)}</div>
                    <div class="text-sm text-gray-500 self-end">/ month on renew</div>
                </div>
            {:else}
                <div class="flex space-x-2">
                    <div>${subscriptionDetails["plan_type_prorated_prices"][selectedPlanType].toFixed(2)}</div>
                    <div class="text-sm text-gray-500 self-end">due now</div>
                </div>
                <div class="flex space-x-2">
                    <div>${subscriptionDetails["plan_type_prices"][selectedPlanType].toFixed(2)}</div>
                    <div class="text-sm text-gray-500 self-end">/ month on renew</div>
                </div>
            {/if}
        </div>

        <Button
            loading={stripePortalLoading}
            classes={planTypeOrder[currentPlanType] > planTypeOrder[selectedPlanType]
                ? "button-base bg-red-500 hover:bg-red-400"
                : "button-base bg-green-500 hover:bg-green-400"}
            on:click={async () => {
                stripePortalLoading = true;
                const data = await changePlan(selectedPlanType, "Credit Card");
                stripePortalLoading = false;
                if (data.url) {
                    window.location = data.url;
                }
                if (data.success) {
                    toast.success(data.success, { duration: 6000 });
                } else if (data.error) {
                    toast.error(data.error, { duration: 6000 });
                }
            }}>
            {#if currentPlanType == "Free"}
                Begin Checkout
            {:else if planTypeOrder[currentPlanType] > planTypeOrder[selectedPlanType]}
                <span class="pr-3 border-r border-gray-300">$0.00</span>
                <span class="ml-3">Downgrade</span>
            {:else}
                <span class="pr-3 border-r border-gray-300">${subscriptionDetails["plan_type_prorated_prices"][selectedPlanType].toFixed(2)}</span>
                <span class="ml-3">Upgrade</span>
            {/if}
        </Button>

        <div class="w-2/3 mt-2 text-sm text-gray-400">*Will use existing Stripe payment method. Click "Open Billing Portal" for more options</div>
    </div>
</Modal>

<DeleteConfirmation
    bind:open={cancelPlanModalOpen}
    deleteCallback={async () => {
        const result = await cancelPlan();
        if (result) {
            toast.success(`We're sorry to see you go 😔, but you still have access until ${subscriptionDetails.renewal_date}`, { duration: 5000 });
        }
    }}>
    <div slot="title">Confirm</div>
    <div slot="description">Are you sure you want to cancel your plan?</div>
    <div slot="cancelText">Back</div>
    <div slot="deleteText">Cancel Plan</div>
</DeleteConfirmation>

<PaymentOptionModal
    bind:open={paymentOptionModalOpen}
    {selectedPlanType}
    {currentPlanType}
    on:openStripePayment={(data) => {
        stripePaymentModalOpen = true;
        stripeClientSecret = data.detail.clientSecret;
        stripeSubscriptionId = data.detail.subscriptionId;
    }} />

<StripePaymentModal bind:open={stripePaymentModalOpen} clientSecret={stripeClientSecret} subscriptionId={stripeSubscriptionId} />
