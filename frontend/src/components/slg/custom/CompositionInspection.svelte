<script>
    import NumberButtonGroup from '../pagination/NumberButtonGroup.svelte'
    import Tooltip from '../informative/Tooltip.svelte'

    export let sortBy = "value";
    export let sortOrder = "descending" // not currently handled but this is the order
    export let contentObject = {'Nonexistent': 0} // object of form {name: time}
    export let example = false;

    export let truncateTo = 30;
    export let tooltip = true;

    export let elementsPerPage = 4;
    export let numPages = Math.ceil(Object.keys(contentObject).length / elementsPerPage);
    export let currentPage = 0;

    function sortObject() {
        if (!contentObject) {
            return {}
        }

        if (sortBy == 'value') {
            let output = {}
            let sortedList = Object.entries(contentObject).sort((a, b) => b[1] - a[1])

            for (let obj of sortedList) {
                output[obj[0]] = convertTime(obj[1]);
            }
            return output
        } else if (sortBy == 'key') {
            let output = {}
            let sortedList = Object.entries(contentObject).sort((a, b) => b[0] - a[0])

            for (let obj of sortedList) {
                output[obj[0]] = convertTime(obj[1]);
            }
            return output
        } else {
            return contentObject;
        }
    }

    function convertTime(seconds) {
        // this means the time has already been converted; useful for 2 way bindings that may result in multiple runs
        if (!seconds.toString().match(/^\d*$/)) {
            return seconds;
        }
        var seconds = parseInt(seconds, 10)
        var hours   = Math.floor(seconds / 3600)
        var minutes = Math.floor((seconds - (hours * 3600)) / 60)
        var seconds = seconds - (hours * 3600) - (minutes * 60)
        if ( !!hours ) {
            if ( !!minutes ) {
            return `${hours}h ${minutes}m ${seconds}s`
            } else {
            return `${hours}h ${seconds}s`
            }
        }
        if ( !!minutes ) {
            return `${minutes}m ${seconds}s`
        }
        return `${seconds}s`
    }


    function range(start, end) {
        let output = []
        for (let i=start; i<end; i++) {
            output.push(i)
        }
        return output
    }
    $: numPages = Math.ceil(Object.keys(contentObject).length / elementsPerPage);
    $: pageNums = range(1, numPages+1);

    $: contentObject = sortObject(contentObject);

</script>

{#if example}

    <svelte:self />

{:else}

    <ul class="mb-4">
        {#each Object.entries(contentObject).slice(parseInt(currentPage * elementsPerPage), parseInt(currentPage * elementsPerPage) + parseInt(elementsPerPage)) as [name, time], i}

            {#if tooltip}
                    <div class="flex justify-between">
                        <Tooltip>
                            <li slot="element"
                                class="cursor-default">
                                {name.substring(0,truncateTo)}{name.length > 30 ? '...' : ''}
                            </li>
                            <div slot="tooltipDiv"
                                class="px-4 py-2 rounded-md z-50 bg-1 shadow-4">
                                {name}
                            </div>
                        </Tooltip>
                        <span>{time}</span>
                    </div>
            {:else}
                <li>{name.substring(0,truncateTo)}{name.length > 30 ? '...' : ''}<span class="float-right">{time}</span></li>
            {/if}
        {/each}
    </ul>

    <div class="flex justify-center">
        <NumberButtonGroup bind:active={currentPage} bind:pageNums={pageNums} />
    </div>

{/if}