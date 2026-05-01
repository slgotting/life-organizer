
<script>
    import SimpleSelect from '../selects/Simple.svelte';
    import Checkbox from '../checkboxes/Checkbox.svelte';

    export let label = '';
    export let description = '';
    export let checked = false;

    export let options = ['Easy', 'Medium', 'Hard'];
    export let value = "";

    export let buttonClasses = "bg-inherit relative w-full border dark:border-gray-700 border-gray-300 dark:text-gray-50 text-gray-800 rounded-md shadow-sm pl-3 pr-10 py-2 text-left cursor-default focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
    export let dropdownClasses = "absolute z-20 mt-1 w-full bg-1 dark:bg-gray-800 bg-white text-gray-800 dark:text-gray-50 shadow-lg max-h-60 rounded-md text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm border-4 border-daw-gray-100"

    let open = false;

    $: closeSelect(checked);

    function closeSelect(checked) {
        if (!checked && open) {
            open = false;
        }
    }
</script>


<div class="flex items-center">
    <div class="mr-2">
        <Checkbox title={label} {description} bind:checked />
    </div>
    <div>
        <SimpleSelect
            label={""}
            {options}
            bind:open
            bind:value
            disabled={!checked}
            {buttonClasses}
            {dropdownClasses}
        />
    </div>
        <!-- <slot /> -->
</div>