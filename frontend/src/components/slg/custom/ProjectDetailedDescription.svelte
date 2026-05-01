<script>
    import TabsUnderline from "../tabs/TabsUnderline.svelte";
    import TabContent from "../tabs/TabContent.svelte";

    export let example = false;

    export let tabNames = ['Implementation Details', 'Specs']
    export let useBuiltinContent = false;

    let selectedIdx;

</script>

{#if example}

    <svelte:self />

{:else}

<TabsUnderline
    {tabNames}
    {useBuiltinContent}
    bind:selectedIdx={selectedIdx}
/>


{#each tabNames as tab, i}

<TabContent >



</TabContent>

    {#if selectedIdx == i}
        <div class="px-4 py-4">
                <div>
                    hey{i}
                </div>
        </div>
    {/if}

{/each}


{/if}