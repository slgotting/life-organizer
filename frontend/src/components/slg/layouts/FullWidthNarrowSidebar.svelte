<script>
    import { fly, slide } from 'svelte/transition';
    import TwoColumnLayout from "./TwoColumnLayout.svelte";
    import LightDark from "../toggles/LightDark.svelte";

    export let breakpoint = "lg";
    export let includeProfile = true;

    export let logo = 'https://tailwindui.com/img/logos/workflow-mark.svg?color=indigo&shade=600';

    console.log(logo);
    let mobileNavHidden = true;

    export let navObjects = [
        {
            href: "charts",
            name: "Charts",
            img: `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
</svg>`,
        },
        {
            href: "calculate",
            name: "Calculate",
            img: `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
</svg>`,
        },
    ];
</script>

<!--
  This example requires updating your template:

  ```
  <html class="h-full bg-gray-50">
  <body class="h-full overflow-hidden">
  ```
-->
<div class="h-full flex bg-1">
    <!-- Off-canvas menu for mobile, show/hide based on off-canvas menu state. -->
    {#if !mobileNavHidden}
    <div
        class="
        flex
        fixed inset-0 z-40"
        role="dialog"
        aria-modal="true">
        <!--
        Off-canvas menu overlay, show/hide based on off-canvas menu state.

        Entering: "transition-opacity ease-linear duration-300"
          From: "opacity-0"
          To: "opacity-100"
        Leaving: "transition-opacity ease-linear duration-300"
          From: "opacity-100"
          To: "opacity-0"
      -->
        <div on:click={() => mobileNavHidden = true} class="fixed inset-0 bg-gray-600 bg-opacity-75" aria-hidden="true" />

        <!--
        Off-canvas menu, show/hide based on off-canvas menu state.

        Entering: "transition ease-in-out duration-300 transform"
          From: "-translate-x-full"
          To: "translate-x-0"
        Leaving: "transition ease-in-out duration-300 transform"
          From: "translate-x-0"
          To: "-translate-x-full"
      -->
        <div
            in:fly|local={{x: -200}}
            class="relative flex-1 flex flex-col max-w-xs w-full bg-1 focus:outline-none">
            <!--
          Close button, show/hide based on off-canvas menu state.

          Entering: "ease-in-out duration-300"
            From: "opacity-0"
            To: "opacity-100"
          Leaving: "ease-in-out duration-300"
            From: "opacity-100"
            To: "opacity-0"
        -->
            <div class="absolute top-0 right-0 -mr-12 pt-4">
                <button
                    on:click={() => mobileNavHidden = !mobileNavHidden}
                    type="button"
                    class="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white">
                    <span class="sr-only">Close sidebar</span>
                    <!-- Heroicon name: outline/x -->
                    <svg class="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <div class="pt-5 pb-4">
                <div class="flex-shrink-0 flex items-center px-4">
                    <a href="/">
                    <img class="h-8 w-auto" src="{ logo }" alt="logo" />
                    </a>
                </div>
                <nav aria-label="Sidebar" class="mt-5">
                    <div class="px-2 space-y-1">
                        {#each navObjects as { href, name, img }, i}
                            <a
                                {href}
                                class="group p-2 rounded-md flex items-center text-base font-medium text-gray-600 hover:bg-gray-50 hover:text-gray-900 dark:hover:bg-gray-900 dark:hover:text-gray-50">
                                <!-- Heroicon name: outline/home -->
                                <div class="text-gray-400 group-hover:text-gray-500 dark:text-gray-500 dark:group-hover:text-gray-400">
                                    {@html img}
                                </div>
                                <div class="ml-4">
                                    {name}
                                </div>
                            </a>
                        {/each}
                    </div>
                </nav>
            </div>
            <div class="flex-shrink-0 flex flex-col border-t border-gray-200 dark:border-gray-800 p-4">
                <div class="flex items-center mb-4">
                    <p class="mr-4">Dark Mode</p>
                    <LightDark />
                </div>

                {#if includeProfile}
                    <a href="#" class="flex-shrink-0 group block">
                        <div class="flex items-center">
                            <div>
                                <img
                                    class="inline-block h-10 w-10 rounded-full"
                                    src="https://images.unsplash.com/photo-1502685104226-ee32379fefbe?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                                    alt="" />
                            </div>
                            <div class="ml-3">
                                <p class="text-base font-medium text-gray-700 group-hover:text-gray-900 dark:text-gray-300 dark:group-hover:text-gray-50">
                                    Emily Selman
                                </p>
                                <p class="text-sm font-medium text-gray-500 group-hover:text-gray-700 dark:text-gray-500 dark:group-hover:text-gray-300">
                                    Account Settings
                                </p>
                            </div>
                        </div>
                    </a>
                {/if}
            </div>
        </div>

        <div class="flex-shrink-0 w-14" aria-hidden="true">
            <!-- Force sidebar to shrink to fit close icon -->
        </div>
    </div>
    {/if}

    <!-- Static sidebar for desktop -->
    <div class="hidden lg:flex lg:flex-shrink-0">
        <div class="flex flex-col w-20">
            <div class="flex-1 flex flex-col min-h-0 overflow-y-auto bg-primary-600">
                <div class="flex-1">
                    <div class="bg-primary-700 py-4 flex items-center justify-center">
                        <a href="/">
                            <img class="h-8 w-auto" src="{ logo }" alt="logo" />
                        </a>
                    </div>
                    <nav aria-label="Sidebar" class="py-6 flex flex-col items-center space-y-3">
                        {#each navObjects as { href, name, img }, i}
                            <a {href} class="flex items-center p-4 rounded-lg text-indigo-200 hover:bg-primary-700">
                                <!-- Heroicon name: outline/home -->
                                {@html img}
                                <span class="sr-only">{name}</span>
                            </a>
                        {/each}
                    </nav>
                </div>
                <div class="relative flex justify-center pb-5">
                    <LightDark condensed={true} moonColorStrength1="800" moonColorStrength2="500" />
                </div>

                {#if includeProfile}
                    <div class="flex-shrink-0 flex pb-5">
                        <a href="#" class="flex-shrink-0 w-full">
                            <img
                                class="block mx-auto h-10 w-10 rounded-full"
                                src="https://images.unsplash.com/photo-1502685104226-ee32379fefbe?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                                alt="" />
                            <div class="sr-only">
                                <p>Emily Selman</p>
                                <p>Account settings</p>
                            </div>
                        </a>
                    </div>
                {/if}
            </div>
        </div>
    </div>

    <div class="flex-1 min-w-0 flex flex-col overflow-auto">
        <!-- Mobile top navigation -->
        <div class="lg:hidden">
            <div class="bg-primary-600 py-2 px-4 flex items-center justify-between sm:px-6 lg:px-8">
                <div>
                    <a href="/">
                        <img class="h-8 w-auto" src="{ logo }" alt="Workflow" />
                    </a>
                </div>
                <div>
                    <button
                        on:click={() => mobileNavHidden = !mobileNavHidden}
                        type="button"
                        class="-mr-3 h-12 w-12 inline-flex items-center justify-center bg-primary-600 rounded-md text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white">
                        <span class="sr-only">Open sidebar</span>
                        <!-- Heroicon name: outline/menu -->
                        <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <TwoColumnLayout {breakpoint}>
            <div slot="left"><slot name="left" /></div>
            <div slot="right"><slot name="right" /></div>
        </TwoColumnLayout>
        <!-- <main class="flex-1 flex overflow-hidden flex-col lg:flex-row">

            <section class="min-w-0 flex-1 h-full flex flex-col overflow-y-auto lg:order-first border-b">
              <slot name="right" />
            </section>

            <aside class="lg:order-first">
              <div class="lg:h-full relative flex flex-col lg:w-96  border-r border-gray-200 overflow-y-auto dark:border-gray-800">
                <slot name="left" />
              </div>
            </aside>
          </main> -->
    </div>
</div>
