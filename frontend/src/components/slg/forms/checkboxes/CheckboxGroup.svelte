<script>
    import Checkbox from './Checkbox.svelte';

    export let componentType = 'inline' // standard, inline, right, simple-right
    export let checkboxes = [
        {
            title: "Example",
            description: "This is an example description",
            checked: false,
        },
        {
            title: "2nd Example",
            description: "This is another example description",
            checked: false,
        },
        {
            title: "Example 3",
            description: "This is the third description",
            checked: false,
        }
    ]

</script>

<fieldset class="space-y-5">
    {#if componentType == 'right'}
        <div class="divide-y divide-gray-200 dark:divide-gray-800">
            {#each checkboxes as checkbox}
                <Checkbox
                    {componentType}
                    title={checkbox.title}
                    description={checkbox.description}
                    bind:checked={checkbox.checked}
                />
            {/each}
        </div>
    {:else if componentType == 'simple-right'}
        <div class="mt-4 border-t border-b border-gray-200 divide-y divide-gray-200 dark:divide-gray-800 dark:border-gray-800">
            {#each checkboxes as checkbox}
                <Checkbox
                    {componentType}
                    title={checkbox.title}
                    description={checkbox.description}
                    bind:checked={checkbox.checked}
                />
            {/each}
        </div>
    {:else}
        {#each checkboxes as checkbox}
            <Checkbox
                {componentType}
                title={checkbox.title}
                description={checkbox.description}
                bind:checked={checkbox.checked}
            />
        {/each}
    {/if}
</fieldset>