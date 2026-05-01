<script>
    import Tree from "./Tree.svelte";

    export let node;

    function addChild() {
        node.children = [
            ...node.children,
            {
                id: crypto.randomUUID(),
                children: []
            }
        ];
    }
</script>

<div style="margin-left: 20px;">
    Node: {node.id}

    {#each node.children as child (child.id)}
        <Tree node={child} />
    {/each}

    <button on:click={addChild}>Add child</button>
</div>