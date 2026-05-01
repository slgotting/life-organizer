
<script>
	// for use with Pagination

	// quite possibly the ugliest implementation of anything ever, in all of history
	// but hey, if its componentized and acts as you expect, is it that big of a deal?

	export let pageNums = [1,2,3,4,5,6,7];
	export let active = 0;

    export let example = false;
    export let activeBackground = "bg-3"

</script>


{#if example}

    <svelte:self />

{:else}

    {#if pageNums.length <= 1}
        <div class="flex space-x-6">
        </div>
    {:else}

    <div class="flex space-x-6">
        {#if active > 0}
        <button on:click={() => active = 0}>
            {pageNums[0]}
        </button>
        {/if}

        {#if active > 2}
        <button>
            ...
        </button>
        {/if}

        {#if active > 1}
        <button on:click={() => active = active - 1}>
            {pageNums[active - 1]}
        </button>
        {/if}

        <!-- active page -->
        <button
            class="text-primary-600 dark:text-primary-400 text-2xl
                    {activeBackground} px-2 rounded"
            style="text-shadow: 1px 1px 1px black;"
        >
            {pageNums[active]}
        </button>

        {#if active < pageNums.length - 2}
        <button on:click={() => active = active + 1}>
            {pageNums[active + 1]}
        </button>
        {/if}

        {#if active < pageNums.length - 3}
        <button>
            ...
        </button>
        {/if}

        {#if active < pageNums.length - 1}
            <button on:click={() => active = pageNums.length - 1}>
                {pageNums[pageNums.length - 1]}
            </button>
        {/if}
    </div>
    {/if}

{/if}
