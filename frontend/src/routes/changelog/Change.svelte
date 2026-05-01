<script>
    export let version = "v1.0.0";
    export let date = "5/30/2024";
    export let changes = [
        "Initial Release"
    ]
</script>

<div class="max-w-80 overflow-x-clip">
    <div class="flex items-center">
        <span class="font-bold">{version}</span>
        <span class="ml-4 dark:text-slate-400 text-slate-700 rounded-md shadow-sm text-sm text-leftself-end">{date}</span>
    </div>
    <ul class="ml-4 text-sm dark:text-slate-300 text-slate-700 font-light">
        {#each changes as change}
        <li>{change}</li>
        {/each}
    </ul>
</div>


<style>
    li:before {
        content:"·";
        margin-right: 0.5rem;
    }
</style>