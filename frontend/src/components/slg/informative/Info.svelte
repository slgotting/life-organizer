<script>

    /**
        * @file Tooltip with little info icon preset
        * @author slgotting
    */

    import { fade } from 'svelte/transition';
    import Tooltip from "./Tooltip.svelte";

    export let example = false

    /**
        * Tailwind described size using both height and width
        * @type {type}
        * @example
        * "h-4 w-4"
    */
    export let size = "h-4 w-4";


    /**
        * Where the tooltip should be positioned
        * @type {string}
        * @example
        * "top"
    */
    export let tooltipPos = 'top'

    export let hideDelay = 150; // ms

    // internally used
    export let _hideTimeout = null;
    export let showTooltip = null;
</script>


{#if example}
    <svelte:self>
        <div in:fade|local={{duration: 400}}
             class="dark:bg-slate-800 bg-white px-4 py-2
                    rounded-md max-w-xs shadow-4">
            <div class="text-sm">
                This is my lidl tooltip
            </div>
        </div>
    </svelte:self>

{:else}

<Tooltip tooltipPos="{tooltipPos}" bind:showTooltip bind:_hideTimeout {hideDelay}>
    <span slot="element">
        <button on:click={(e) => e.preventDefault()}>
            <svg xmlns="http://www.w3.org/2000/svg" class="{size} fill-slate-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
        </button>
    </span>

    <div slot="tooltipDiv" class="z-50"
        role="tooltip"
        on:mouseenter={() => {
            clearTimeout(_hideTimeout);
        }}
        on:mouseleave={() => {
            _hideTimeout = setTimeout(() => {
                // clearTimeout(debounceTimeout);
                showTooltip = false;
            }, hideDelay);
        }}
    >
        <slot />
    </div>
</Tooltip>

{/if}