<script>

    export let example = false;

    export let href = "#"
    export let text = "Visit"
    export let direction = "right"

</script>

{#if example}

    <svelte:self />

{:else}

    {#if direction == "right"}
    <a href="{href}" class="flex" target="_blank">
        {text}
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 rotate-45 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8 7l4-4m0 0l4 4m-4-4v18" />
        </svg>
    </a>
    {:else if direction == "left"}
    <a href="{href}" class="flex" target="_blank">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 -rotate-45 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8 7l4-4m0 0l4 4m-4-4v18" />
        </svg>
        {text}
    </a>
    {/if}


{/if}