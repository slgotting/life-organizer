<script>
    import LightDark from "../../toggles/LightDark.svelte";
    import { slide, fade, scale, draw, crossfade, blur, fly } from 'svelte/transition';

    export let example = false;
    export let logo="https://tailwindui.com/img/logos/workflow-mark-indigo-600.svg"
    export let includeLogo = true;
    export let includeDarkToggle = true;

    export let navObjects = [
        { href: "#", name: "Dashboard" },
        { href: "#", name: "Team" },
        { href: "#", name: "Projects" },
        { href: "#", name: "Calendar" },
    ];

    let open = false;

    export let rightSide = "contact"; // contact, login
    export let rightSideHref = "#contact"
</script>


<div class="max-w-7xl mx-auto px-4 sm:px-6">

    <nav class="relative flex items-center justify-between sm:h-10 md:justify-center" aria-label="Global">
        <div class="flex items-center flex-1 md:absolute md:inset-y-0 md:left-0">
            <div class="flex items-center justify-between w-full md:w-auto">
                <a href="#">
                    <span class="sr-only">Workflow</span>
                    <img class="h-8 w-auto sm:h-10" src="{ logo }" alt="" />

                </a>
                <div class="-mr-2 flex items-center md:hidden">
                    <button
                        type="button"
                        on:click={() => open = true}
                        class="bg-2 rounded-md p-2 inline-flex items-center justify-center text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
                        aria-expanded="false">
                        <span class="sr-only">Open main menu</span>
                        <!-- Heroicon name: outline/menu -->
                        <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        <div class="hidden md:flex md:space-x-10">
            {#each navObjects as obj}
            <a href="{ obj.href }" class="font-medium text-gray-500 hover:text-gray-900 hover:dark:text-gray-100">{obj.name}</a>
            {/each}
        </div>
        <div class="hidden md:absolute md:flex md:items-center md:justify-end md:inset-y-0 md:right-0">
            <span class="mr-12 mb-1">
                <LightDark condensed=true />
            </span>
            <span class="inline-flex rounded-md shadow">
                {#if rightSide == "login"}
                    <a
                        href="{rightSideHref}"
                        class="inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md text-primary-600 bg-white hover:bg-gray-50">
                        Log in
                    </a>
                {:else if rightSide == "contact"}
                    <a
                        href="{rightSideHref}"
                        class="inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md text-primary-600 bg-white hover:bg-gray-50"
                        >Contact</a>
                {/if}
            </span>
        </div>
    </nav>
</div>



{#if open}
<div
    in:fly|local={{ y: -100, duration: 500 }}
    out:fly|local={{ x: 100, duration: 300 }}
    class="absolute z-10 top-0 inset-x-0 p-2 transition transform origin-top-right md:hidden">
    <div class="rounded-lg shadow-md bg-2 ring-1 ring-black ring-opacity-5 overflow-hidden">
        <div class="px-5 pt-4 flex items-center justify-between">
            <div>
                <img class="h-8 w-auto" src="https://tailwindui.com/img/logos/workflow-mark-primary-600.svg" alt="" />
            </div>
            <div class="-mr-2">
                <button
                    type="button"
                    on:click={() => open = false}
                    class="bg-3 rounded-md p-2 inline-flex items-center justify-center text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500">
                    <span class="sr-only">Close menu</span>
                    <!-- Heroicon name: outline/x -->
                    <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
        </div>
        <div class="px-2 pt-2 pb-3">
            {#each navObjects as obj}
            <a href="{ obj.href }" class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-200 hover:dark:text-gray-50 dark:hover:bg-gray-900">{ obj.name }</a>
            {/each}

            <div class="flex items-center space-x-4">
                <div class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-200 hover:dark:text-gray-50 dark:hover:bg-gray-900">
                    Dark mode
                </div>
                <LightDark />
            </div>
        </div>

        {#if rightSide == "login"}
            <a href="{rightSideHref}" class="block w-full px-5 py-3 text-center font-medium text-primary-600 dark:text-primary-400 bg-1 hover:bg-gray-100 hover:dark:bg-gray-800"> Log in </a>
        {:else if rightSide == "contact"}
            <a href="{rightSideHref}" class="block w-full px-5 py-3 text-center font-medium text-primary-600 dark:text-primary-400 bg-1 hover:bg-gray-100 hover:dark:bg-gray-800">Contact</a>
        {/if}
    </div>
</div>
{/if}

<!-- #endregion Mobile Menu -->
