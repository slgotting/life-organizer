<script>
    import NestedTreeNavLeft from "../NestedTreeNavLeft.svelte";

    export let treeObject = {};
</script>


<div class="flex">
    <NestedTreeNavLeft {treeObject} />
    <slot></slot>
</div>