<script>
    import { slide, fade, scale, draw, crossfade, blur, fly } from 'svelte/transition';

    export let example = false;
    export let startIdx = 0;
    export let variableIdx = 0;

</script>

{#if example}

    <svelte:self />

{:else}

    {#if startIdx == variableIdx}
    <div>
        <slot />
    </div>
    {/if}

{/if}