<script>
    export let componentType = "inline"; // standard, inline, right, simple-right
    export let checked = false;
    export let title = "Title";
    export let description = "This is an example description";
    export let id="comments";
</script>

{#if componentType == "inline"}
    <div class="relative flex items-center">
        <div class="flex items-center h-5">
            <input
                id={id}
                aria-describedby="{id}-description"
                name={id}
                type="checkbox"
                class="focus:ring-primary-500 h-4 w-4 text-primary-600 dark:text-primary-500 border-gray-300 rounded"
                bind:checked={checked} />
        </div>
        <div class="ml-2">
            <label for={id} class="font-medium text-gray-700 dark:text-gray-300">{title}</label>
            <span id="{id}-description" class="text-gray-500"><span class="sr-only">{title} </span>{description}</span>
        </div>
    </div>
{:else if componentType == "standard"}
    <div class="relative flex items-start">
        <div class="flex items-center h-5">
            <input
                id={id}
                aria-describedby="{id}-description"
                name={id}
                type="checkbox"
                class="focus:ring-primary-500 h-4 w-4 text-primary-600 dark:text-primary-500 border-gray-300 rounded" />
        </div>
        <div class="ml-3">
            <label for={id} class="font-medium text-gray-700 dark:text-gray-300">{title}</label>
            <span id="{id}-description" class="text-gray-500"><span class="sr-only">{title}</span>{description}</span>
        </div>
    </div>
{:else if componentType == "right"}
    <div class="relative flex items-start py-4">
        <div class="min-w-0 flex-1">
            <label for={id} class="font-medium text-gray-700 dark:text-gray-300">{title}</label>
            <p id="{id}-description" class="text-gray-500">{description}</p>
        </div>
        <div class="ml-3 flex items-center h-5">
            <input
                id={id}
                aria-describedby="{id}-description"
                name={id}
                type="checkbox"
                class="focus:ring-primary-500 h-4 w-4 text-primary-600 dark:text-primary-500 border-gray-300 rounded" />
        </div>
    </div>
{:else if componentType == "simple-right"}
    <div class="relative flex items-start py-4">
        <div class="min-w-0 flex-1">
            <label for="person-1" class="font-medium text-gray-700 dark:text-gray-300 select-none">{title}</label>
        </div>
        <div class="ml-3 flex items-center h-5">
            <input id="person-1" name="person-1" type="checkbox" class="focus:ring-primary-500 h-4 w-4 text-primary-600 dark:text-primary-500 border-gray-300 rounded" />
        </div>
    </div>
{/if}
