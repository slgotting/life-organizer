<script>
    import Button from "../slg/primitives/Button.svelte";

    export let headline = "Pricing plans for teams of&nbsp;all&nbsp;sizes"
    export let description = "Choose an affordable plan that’s packed with the best features for engaging your audience, creating customer loyalty, and driving sales."

    export let paymentOptions = ["monthly", "annually"]

    export let selectedPriceOption = "monthly"

    export let freePlanAddition = false;

    export let options = [
        { 'title': 'Basic', 'description': '',
            'prices': {
                'monthly': '4',
            },
            'features': [
                '<span class="">Unlimited GPT-3.5 queries</span>',
                '<span class="">No advertisements</span>',
            ],
            'redirect': '/signup?plan=Basic'
        },
        {
            'title': 'Cultivating',
            'prices': {
                'monthly': '8',
            },
            'features': [
                '<span class="">Unlimited GPT-3.5 queries</span>',
                '<span class="">200 GPT-4o queries</span>',
                '<span class="">No advertisements</span>',
                '<span class="">Custom Notifications</span>',
                '<span class="">Dashboard Access</span>',
            ],
            'redirect': '/signup?plan=Cultivating'
        },
        {
            'title': 'Learned',
            'prices': {
                'monthly': '12',
            },
            'features': [
                '<span class="">Unlimited GPT-3.5 queries</span>',
                '<span class="">Unlimited GPT-4o queries</span>',
                '<span class="">No advertisements</span>',
                '<span class="">Custom Notifications</span>',
                '<span class="">Dashboard Access</span>',
            ],
            'redirect': '/signup?plan=Learned'
        },
    ]

    function capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

</script>

<div class="bg-gray-900 py-24 sm:py-32">
    <div class="mx-auto max-w-7xl px-6 lg:px-8">
        <div class="mx-auto max-w-4xl text-center">
            <h2 class="text-base font-semibold leading-7 text-indigo-400">Pricing</h2>
            <p class="mt-2 text-4xl font-bold tracking-tight text-white sm:text-5xl">{@html headline}</p>
        </div>
        <p class="mx-auto mt-6 max-w-2xl text-center text-lg leading-8 text-gray-300">
            {@html description}
        </p>
        <div class="mt-16 flex justify-center">
            <fieldset aria-label="Payment frequency">
                {#if paymentOptions.length === 2}
                <div class="grid grid-cols-2 gap-x-1 rounded-full bg-white/5 p-1 text-center text-sm font-semibold leading-5 text-white">
                    <!-- Checked: "bg-indigo-500" -->
                    <label class="cursor-pointer rounded-full px-2.5 py-1">
                        <input type="radio" name="frequency" value="monthly" class="sr-only" />
                        <span>Monthly</span>
                    </label>
                    <!-- Checked: "bg-indigo-500" -->
                    <label class="cursor-pointer rounded-full px-2.5 py-1">
                        <input type="radio" name="frequency" value="annually" class="sr-only" />
                        <span>Annually</span>
                    </label>
                </div>
                {:else}
                <label class="cursor-pointer rounded-full px-2.5 py-1 bg-indigo-500 text-sm font-semibold leading-5 text-white">
                    <input type="radio" name="frequency" value="annually" class="sr-only" />
                    <span>{capitalize(paymentOptions[0])}</span>
                </label>
                {/if}
            </fieldset>
        </div>
        <div class="isolate mx-auto mt-10 grid max-w-md grid-cols-1 gap-8 lg:mx-0 lg:max-w-none lg:grid-cols-3">
            {#each options as option}
            <div class="rounded-3xl p-8 ring-1 ring-white/10 xl:p-10">
                <div class="flex items-center justify-between gap-x-4">
                    <h3 id="tier-freelancer" class="text-lg font-semibold leading-8 text-white">{option.title}</h3>
                </div>
                <p class="mt-4 text-sm leading-6 text-gray-300">{option.description}</p>
                <p class="mt-6 flex items-baseline gap-x-1">
                    <!-- Price, update based on frequency toggle state -->
                    <span class="text-4xl font-bold tracking-tight text-white">${option.prices[selectedPriceOption]}</span>
                    <!-- Payment frequency, update based on frequency toggle state -->
                    <span class="text-sm font-semibold leading-6 text-gray-300">/month</span>
                </p>
                <a
                    href={option.redirect}
                    aria-describedby="tier-freelancer"
                    class="mt-6 block rounded-md bg-white/10 px-3 py-2 text-center text-sm font-semibold leading-6 text-white hover:bg-white/20 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
                    >Buy plan</a>
                <ul role="list" class="mt-8 space-y-3 text-sm leading-6 text-gray-300 xl:mt-10">
                    {#each option.features as feature}
                    <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none text-white" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path
                                fill-rule="evenodd"
                                d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                                clip-rule="evenodd" />
                        </svg>
                        {@html feature}
                    </li>
                    {/each}
                </ul>
            </div>
            {/each}
        </div>
    {#if freePlanAddition}
        <div class="w-full flex flex-col items-center mt-6">
            <div class="text-sm text-gray-500 mb-2">or continue with the Free Plan</div>
            <Button
                size={'unset'}
                classes={`
                    w-[200px] h-12 text-center items-center px-3 py-2 text-2xl tracking-tight rounded-md
                    font-extrabold shadow-sm text-white focus:outline-none focus:ring-2 focus:ring-offset-2
                    bg-gradient-to-r hover:to-blue-300 hover:from-blue-400 to-blue-400 from-blue-500 focus:ring-blue-500
                    disabled:bg-gradient-to-r disabled:from-gray-500 disabled:to-gray-600 hover:disabled:from-gray-500 hover:disabled:to-gray-600
                `}
                on:click={() => { window.location.href = "/signup" }}>
                <div class="">
                    Sign up
                </div>
            </Button>
        </div>
    {/if}
    </div>

</div>
