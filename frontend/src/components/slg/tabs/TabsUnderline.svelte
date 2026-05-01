<script>
    import { fly,slide } from "svelte/transition";
    export let tabNames = ["My Account", "Company", "Team Members", "Billing"];
    export let tabContent = [
        "<div class='border-2 border-dashed px-4 py-4'>My Account</div>",
        "<div class='border-2 border-dashed px-4 py-4'>Company</div>",
        "<div class='border-2 border-dashed px-4 py-4'>Team Members</div>",
        "<div class='border-2 border-dashed px-4 py-4'>Billing</div>",
    ]
    export let useBuiltinContent = true;
    export let selectedIdx = 0;
    export let breakpoint = "md";
    export let example = false;
    export let activeTab;

    let select;
    $: activeTab = tabNames[selectedIdx];

    let visible = true
    function changeTab() {
        // create fake false/true for animation
        visible = false;
        setTimeout(() => {
            visible = true;
        }, 30);
    }

</script>

<!-- No purge section -->
<!--
sm:block
md:block
lg:block
sm:hidden
md:hidden
lg:hidden
-->

{#if example}

    <svelte:self />

{:else}
<div>
    <div class="{breakpoint}:hidden">
        <label for="tabs" class="sr-only">Select a tab</label>
        <!-- Use an "onChange" listener to redirect the user to the selected tab URL. -->
        <select
            bind:this={select}
            on:change={() => {
                changeTab();
                selectedIdx = select.selectedIndex;
            }}
            class="block w-full pl-3 pr-10 py-2 text-base border border-gray-300 dark:border-gray-800
                   bg-inherit dark:text-primary-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md
            ">
            {#each tabNames as tabName, i}
                <option class="dark:bg-slate-900 bg-slate-50" selected={i == selectedIdx}>{tabName}</option>
            {/each}
        </select>
    </div>
    <div class="hidden {breakpoint}:block">
        <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-8 overflow-x-auto" aria-label="Tabs">
                {#each tabNames as tabName, i}
                    {#if selectedIdx == i}
                        <button
                            bind:this={activeTab}
                            class="dark:border-primary-300 dark:text-primary-400 border-primary-500
                                  text-primary-600 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm
                                    focus-visible:outline-none"
                            aria-current="page">
                            {tabName}
                        </button>
                    {:else}
                        <button
                            on:click={() => {
                                changeTab();
                                selectedIdx = i;
                            }}
                            class="border-transparent text-gray-500 dark:hover:text-gray-300 hover:text-gray-700
                                 hover:border-gray-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm">
                            {tabName}
                        </button>
                    {/if}
                {/each}
            </nav>
        </div>
    </div>
</div>

    {#if useBuiltinContent == true}
        <!-- Content area -->

        {#if visible}

        <div
            in:slide|local
            class="mt-2">

        {@html tabContent[selectedIdx]}

        </div>
        {:else}

        <div
            class="invisible mt-2">

        {@html tabContent[selectedIdx]}

        </div>

        {/if}

    {/if}

{/if}