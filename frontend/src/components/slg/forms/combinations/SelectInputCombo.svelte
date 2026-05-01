<script>
    import SimpleSelect from '../selects/Simple.svelte';
    import SimpleInput from '../inputs/Simple.svelte';

    export let options = ['String', 'Regex'];
    export let label = '';
    export let value = "";
    export let selectValue = "";
    export let selectedIndex = 0;
</script>



<div class="flex items-center">
    <div class="mr-2">
        <SimpleSelect {label} {options} bind:value={selectValue} />
    </div>
    <div>
        <SimpleInput {label} bind:value={value} />
    </div>
        <slot />
</div>