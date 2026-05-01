<script>
    import { onMount } from "svelte";
    import { slide, fade, scale, draw, crossfade, blur, fly } from "svelte/transition";
    import { spring } from "svelte/motion";

    export let folderName = "";
    export let treeObject = {};
    export let depth = 0;

    export let accordionButtonColor = "dark:text-primary-400 text-primary-500";
    export let contentColor = "dark:text-primary-200 text-primary-800";

    export let open = false;
    //   let leaves = treeObject.leaves;
    //   delete treeObject.leaves;
    //   let nodes = treeObject;

    let leaves = [];
    let nodes = {};

    // sort the entries
    const treeObjectSorted = Object.fromEntries(Object.entries(treeObject).sort());

    for (let [key, value] of Object.entries(treeObjectSorted)) {
        if (key == "leaves") {
            leaves = value;
            // sort leaves by the name property in the list of leaf objects
            leaves.sort((a, b) => (a.name > b.name ? 1 : -1));
        } else {
            nodes[key] = value;
        }
    }

    if (depth == 0) {
        open = true;
    }

    //   $: logleaves(open);

    function logleaves(open) {
        console.log(leaves);
        console.log(nodes);
    }
</script>

{#if folderName.length > 0}
    <button
        class="
            flex mx-2 my-2 items-center
            cursor-pointer
            {accordionButtonColor}
        "
        on:click={() => (open = !open)}>
        <span class="mr-2">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4 transform {open ? '' : 'rotate-180'}
                        transition duration-300"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
        </span>
        {folderName}
    </button>
{/if}

{#if open}
    <ul
        transition:slide|local={{duration:500}}

        class="flex-col overflow-hidden
                {depth < 1 ? '' : 'border-l dark:border-gray-700 border-gray-200'}"
        style={depth < 1 ? "" : "margin-left:1.0em;padding-left:0.5em;"}>
        {#each leaves as leaf}
            {#if leaf.href}
            <a href="{leaf.href}"><li class="px-2 pr-6 py-1 cursor-pointer text-sm {contentColor} overflow-hidden">{leaf.name}</li></a>
            {:else}
            <li class="px-2 pr-6 py-1 cursor-pointer text-sm {contentColor} overflow-hidden">{leaf.name}</li>
            {/if}
        {/each}

        {#each Object.keys(nodes) as node}
            <svelte:self folderName={node} treeObject={nodes[node]} depth={depth + 1} />
        {/each}
    </ul>
{/if}

        <!-- transition:slide -->
        <!-- in:fade -->