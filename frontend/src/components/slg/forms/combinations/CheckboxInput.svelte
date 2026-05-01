
<script>
    import SimpleInput from '../inputs/Simple.svelte';
    import Checkbox from '../checkboxes/Checkbox.svelte';

    export let id = "comments"
    export let label = '';
    export let description = '';
    export let placeholder = '';
    export let checked = false;

    export let value = "";

    export let inputClasses = "px-3 py-2 bg-inherit border border-gray-300 dark:border-gray-700  focus:ring-primary-500 focus:border-primary-500 block w-full"

</script>


<div class="flex items-center">
    <div class="mr-2">
        <Checkbox id={id} title={label} {description} bind:checked />
    </div>
    <div>
        <SimpleInput
            label={""}
            bind:value
            {placeholder}
            disabled={!checked}
            {inputClasses}
        />
    </div>
        <!-- <slot /> -->
</div>