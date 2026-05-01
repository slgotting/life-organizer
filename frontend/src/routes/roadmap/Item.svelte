<script>
    export let name = "v1.0.0";
    export let items = [
        "Initial Release"
    ]
</script>

<div class="max-w-80 overflow-x-clip">
    <div class="flex items-center">
        <span class="font-bold">{name}</span>
    </div>
    <ul class="ml-4 text-sm dark:text-slate-300 text-slate-700 font-light">
        {#each items as item}
        {@html item}
        {/each}
    </ul>
</div>


<style>
    li:before {
        content:"·";
        margin-right: 0.5rem;
    }
</style>