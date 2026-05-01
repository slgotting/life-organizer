<script>

    export let example = false;

    export let href="#"
</script>

{#if example}

    <svelte:self>
        Example link
    </svelte:self>

{:else}

<a {href}
    class="w-fit dark:text-primary-400 hover:dark:text-primary-300 text-primary-700 hover:text-primary-600">
    <slot />
</a>

{/if}