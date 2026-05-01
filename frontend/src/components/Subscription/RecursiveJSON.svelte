<!-- @format -->
<script>
    import { onMount } from "svelte";

    export let data = {
        'Custom Notifs': false,
        'Dashboard Access': false,
        'No Advertisements': true,
        'Credits': {
            'gpt-4o-mini': 100,
            'gpt-4': {
                'o': 100,
                'i': 100,
            },
        }
    };

    export let autoUpdateWidth = false;

    export let keyFormattingFunction = (val) => val;
    export let valueFormattingFunction = (val) => val;

    export let valueClass = "text-xs text-blue-500";
    export let keyClass = "text-xs";

    export let nestLevel = 0;

    onMount(() => {

        if (autoUpdateWidth) {
            let largest = 0;
            document.querySelectorAll(`.key-${nestLevel}`).forEach((elem) => {
                const w = elem.offsetWidth;
                if (w > largest) {
                    largest = w;
                }
            })

            // apply width to each element
            document.querySelectorAll(`.key-${nestLevel}`).forEach((elem) => {
                elem.style.width = `${largest + 6 }px`;
            })
        }
    })
</script>

<div class="pl-4 flex flex-col space-y-1">
{#each Object.entries(data) as [k, v]}
    {#if typeof v === "object"}
        <div><span class={keyClass}>{@html keyFormattingFunction(k)}</span></div>
        <svelte:self
            data={v}
            {keyFormattingFunction}
            {valueFormattingFunction}
            nestLevel={nestLevel+1}
            {autoUpdateWidth}
            {keyClass}
            {valueClass}
        />
    {:else}
        <div class="flex space-x-2 items-center">
            <div class="border-r border-gray-700 key-{nestLevel}"><span class={keyClass}>{@html keyFormattingFunction(k)}</span></div>
            <div><span class={valueClass}>{@html valueFormattingFunction(v)}</span></div>
        </div>
    {/if}
{/each}
</div>

<!-- <ul class="pl-4">
    {#each Object.entries(data) as [k, v]}
        {#if typeof v === "object"}
            <li><span class={keyClass}>{@html keyFormattingFunction(k)}</span></li>
            <svelte:self data={v} {keyFormattingFunction} {valueFormattingFunction} />
        {:else}
            <li><span class={keyClass}>{@html keyFormattingFunction(k)}</span></li>
            <li><span class={valueClass}>{@html valueFormattingFunction(v)}</span></li>
        {/if}
    {/each}
</ul>
 -->


<!-- <table border="1" class="mt-24">
    <tbody>
    {#each Object.entries(data) as [k, v]}
        {#if typeof v === "object"}
        <tr>
            <td><span class={keyClass}>{@html keyFormattingFunction(k)}</span></td>
            <td><svelte:self data={v} {keyFormattingFunction} {valueFormattingFunction} /></td>
        </tr>
        {:else}
        <tr>
            <td><span class={keyClass}>{@html keyFormattingFunction(k)}</span></td>
            <td><span class={valueClass}>{@html keyFormattingFunction(v)}</span></td>
        </tr>
        {/if}
    {/each}
    </tbody>
</table> -->
