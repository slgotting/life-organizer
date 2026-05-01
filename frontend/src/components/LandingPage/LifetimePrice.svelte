<script>
    import DescriptionWithArrowRight from "../slg/handdrawn/DescriptionWithArrowRight.svelte";
    import DescriptionWithArrowUp from "../slg/handdrawn/DescriptionWithArrowUp.svelte";

    // 6 means July; devs really couldnt have bumped the index (jfc)
    const offerExpirationDate = new Date(2024,6,30,6,30,0);

    const expirationDate = '9/30/24'

    export let price = '$40'
</script>

    <div class="mx-auto max-w-7xl px-6 lg:px-8 py-24 sm:py-32">
        <!-- <div class="mx-auto max-w-2xl sm:text-center">
            <h2 class="text-3xl font-bold tracking-tight text-daw-gray-900 sm:text-4xl">Simple no-tricks pricing</h2>
            <p class="mt-6 text-lg leading-8 text-daw-gray-600">
                Distinctio et nulla eum soluta et neque labore quibusdam. Saepe et quasi iusto modi velit ut non voluptas in. Explicabo id ut laborum.
            </p>
        </div> -->
        <div class="mx-auto mt-16 max-w-2xl rounded-3xl ring-1 ring-daw-gray-200 sm:mt-20 lg:mx-0 lg:flex lg:max-w-none">
            <div class="p-8 sm:p-10 lg:flex-auto">
                <h3 class="text-2xl font-bold tracking-tight text-daw-gray-900">Lifetime membership</h3>
                <p class="mt-6 text-base leading-7 text-daw-gray-600">
                    Limited time offer to show your support and gain permanent access to all future premium features
                </p>
                <div class="mt-10 flex items-center gap-x-4">
                    <h4 class="flex-none text-sm font-semibold leading-6 text-daw-emerald-600">What’s included</h4>
                    <div class="h-px flex-auto bg-daw-gray-100"></div>
                </div>
                <ul role="list" class="mt-8 grid grid-cols-1 gap-4 text-sm leading-6 text-daw-gray-600 sm:grid-cols-2 sm:gap-6">
                    <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none text-daw-emerald-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path
                                fill-rule="evenodd"
                                d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                                clip-rule="evenodd" />
                        </svg>
                        Unlimited GPT-4o queries
                    </li>
                    <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none text-daw-emerald-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path
                                fill-rule="evenodd"
                                d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                                clip-rule="evenodd" />
                        </svg>
                        Access to all current and future features
                    </li>
                    <!-- <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none text-daw-emerald-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path
                                fill-rule="evenodd"
                                d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                                clip-rule="evenodd" />
                        </svg>
                        Access to all future premium features
                    </li> -->
                    <!-- <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none text-daw-emerald-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path
                                fill-rule="evenodd"
                                d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                                clip-rule="evenodd" />
                        </svg>
                        Entry to annual conference
                    </li>
                    <li class="flex gap-x-3">
                        <svg class="h-6 w-5 flex-none text-daw-emerald-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path
                                fill-rule="evenodd"
                                d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                                clip-rule="evenodd" />
                        </svg>
                        Official member t-shirt
                    </li> -->
                </ul>
            </div>
            <div class="-mt-2 p-2 lg:mt-0 lg:w-full lg:max-w-md lg:flex-shrink-0">
                <div class="rounded-2xl bg-daw-gray-100 py-10 text-center lg:flex lg:flex-col lg:justify-center lg:py-16">
                    <div class="relative mx-auto max-w-xs px-8">
                        <p class="text-base font-semibold text-daw-gray-600">Pay once, own it forever</p>
                        <p class="mt-6 flex items-baseline justify-center gap-x-2">
                            <span class="text-5xl font-bold tracking-tight text-daw-gray-900">{price}</span>
                            <span class="text-sm font-semibold leading-6 tracking-wide text-daw-gray-600">USD</span>
                        </p>
                        <div class="sm:hidden absolute top-32 left-24">
                            <DescriptionWithArrowUp>
                                <div class="relative -right-10 top-28 text-red-500 text-sm w-12" style="font-family: handwritten; text-shadow: 1px 1px 4px black;">
                                    Offer expires {expirationDate}
                                </div>
                            </DescriptionWithArrowUp>
                        </div>
                        <div class="hidden sm:block absolute -left-16 top-12">
                            <DescriptionWithArrowRight>
                                <div class="relative -left-12 top-16 text-red-500 text-sm w-12" style="font-family: handwritten; text-shadow: 1px 1px 4px black;">
                                    Offer expires {expirationDate}
                                </div>
                            </DescriptionWithArrowRight>
                        </div>
                        <a
                            href="#"
                            class="mt-10 block w-full rounded-md bg-daw-emerald-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-daw-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                            >Get access</a>
                        <!-- <p class="mt-6 text-sm leading-5 text-daw-gray-600">Invoices and receipts available for easy company reimbursement</p> -->
                    </div>
                </div>
            </div>
        </div>
    </div>