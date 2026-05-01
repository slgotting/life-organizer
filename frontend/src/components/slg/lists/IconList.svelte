<script>
    import Tooltip from '../informative/Tooltip.svelte';
    import { fade } from 'svelte/transition';

    export let example = false;

    export let height = "h-16";
    export let bgColor = "bg-slate-800 dark:bg-white";
    export let ringColor = "dark:ring-gray-900 ring-white"
    export let ringSize = "ring-8"

    export let baseDir = "/static/icons";
    export let includeTooltip = true;

    export let icons = [
        "Svelte",
        "Kubernetes",
        "Github Actions",
        "MongoDB",
        "Github",
    ]


</script>

{#if example}

    <svelte:self />

{:else}

    {#if includeTooltip}

    <div class="flex overflow-hidden -space-x-2 p-2 bg-inherit ring-current">
        {#each icons as icon, i}
            <Tooltip tooltipPos="top">
                <img slot="element" class="inline-block {height} {bgColor} {ringColor} {ringSize} border-4 border-transparent rounded-full" src="{ baseDir }/{ icon }.svg" alt="{ icon }">

                <div slot="tooltipDiv"
                        in:fade|local={{duration: 400}}
                        class="dark:bg-slate-800 bg-white px-4 py-2 rounded-md z-50 shadow-4">
                    {icon}
                </div>
            </Tooltip>
        {/each}
    </div>

    {:else}

    <div class="flex overflow-hidden -space-x-2 p-2 bg-inherit ring-current">
        {#each icons as icon, i}
                <img class="inline-block {height} {bgColor} {ringColor} {ringSize} border-4 border-transparent rounded-full" src="{ baseDir }/{ icon }.svg" alt="{ icon }">
        {/each}
    </div>

    {/if}

{/if}