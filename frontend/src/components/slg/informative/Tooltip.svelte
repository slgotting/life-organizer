<script>
    import { slide, fade, scale, draw, crossfade, blur, fly } from "svelte/transition";
    import { createPopperActions } from "svelte-popperjs";
    const [popperRef, popperContent] = createPopperActions();


    const DEFAULTS = {
        'top': {
            placement: 'top',
            modifiers: [{ name: "offset", options: { offset: [0, 8] } }],
        },
        'left': {
            placement: 'left',
            modifiers: [{ name: "offset", options: { offset: [0, 8] } }],
        },
        'right': {
            placement: 'right',
            modifiers: [{ name: "offset", options: { offset: [0, 8] } }],
        },
    }

    export let tooltipPos = 'top';
    export let debounceTime = 250; // ms

    export let hideDelay = 150; // ms

    export let _hideTimeout = null;

    let popperOptions

    if (tooltipPos) {
        popperOptions = DEFAULTS[tooltipPos];
    }

    let debounceTimeout;
    export let showTooltip = false;

    export let example = false;
</script>


{#if example}
    <svelte:self tooltipPos="top">
        <button class="" slot="element">Test button</button>
        <div slot="tooltipDiv"
                in:fade|local={{duration: 400}}
                class="dark:bg-slate-800 bg-white px-4 py-2 rounded-md z-50">
            This is the tooltip text!
        </div>
    </svelte:self>

{:else}

<div style="height:fit-content; width:fit-content;"
    role="tooltip"
    use:popperRef
    on:mouseenter={() => {
        clearTimeout(_hideTimeout);
        debounceTimeout = setTimeout(() => {
            showTooltip = true;
        }, debounceTime);
    }}
    on:mouseleave={() => {
        _hideTimeout = setTimeout(() => {
            clearTimeout(debounceTimeout);
            showTooltip = false;
        }, hideDelay);
    }}
    on:touchstart={() => {
        clearTimeout(_hideTimeout);
        showTooltip = true;
    }}
>
    <slot name="element" />
    {#if showTooltip}
        <div
            use:popperContent={popperOptions}
            style="z-index: 9999;">
            <slot name="tooltipDiv" />
        </div>
    {/if}
</div>

{/if}
