
<script>
    import RecursiveJson from "./RecursiveJSON.svelte";

    export let keyClass;
    export let valueClass;
    export let planName = "Free"
    export let planAccess = {
        'Custom Notifs': false,
        'Dashboard Access': false,
        'No Advertisements': true,
        'Credits': {
            'gpt-4o-mini': 100,
        }
    }
    export let autoUpdateWidth;

    const SYMBOL_MAP = {
        true: "<span class='text-xl text-green-500'>✓</span>",
        false: "<span class='text-red-500'>✕</span>",
        'unlimited': "<span class='text-xl text-green-500'>∞</span>",
        'gpt-3_5': 'ChatGPT - 3.5',
        'gpt-4o-mini': 'ChatGPT - 4o mini',
        'gpt-4o': 'ChatGPT - 4o',
    }

    function toSymbol(val) {
        if (val in SYMBOL_MAP) {
            return SYMBOL_MAP[val];
        } else {
            return val;
        }
    }

</script>

<div class="flex flex-col space-y-2">
    <div class="pl-8">{planName}</div>

    <RecursiveJson
        data={planAccess}
        keyFormattingFunction={toSymbol}
        valueFormattingFunction={toSymbol}
        {keyClass}
        {valueClass}
        {autoUpdateWidth}
    />

    <!-- <ul>
    {#each Object.entries(planAccess) as [k,v]}
        {#if typeof v === 'object'}
            <li>{k}</li>
            <ul class="pl-4">
            {#each Object.entries(v) as [key,val]}
                <li>
                    {key} - {to_symbol(val)}
                </li>
            {/each}
            </ul>
        {:else}
            <li>{k} - {to_symbol(v)}</li>
        {/if}
    {/each}
    </ul> -->

</div>
