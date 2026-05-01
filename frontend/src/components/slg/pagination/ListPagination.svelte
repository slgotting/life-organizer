<script>
    import NumberButtonGroup from './NumberButtonGroup.svelte'

    export let example = false;

    // all elements will be included in an opinionated manner until a better solution is thought up
    export let elements = [

    ]
    export let elementsPerPage = 4;
    export let numPages = Math.ceil(elements.length / elementsPerPage);
    export let currentPage = 1;

    function range(start, end) {
        let output = []
        for (let i=start; i<end; i++) {
            output.push(i)
        }
        return output
    }
    $: numPages = Math.ceil(elements.length / elementsPerPage);
    $: pageNums = range(1, numPages+1);

</script>


{#if example}

    <svelte:self elements={[
        '<li>elem1<span class="float-right">29</span></li>',
        '<li>elem2<span class="float-right">29</span></li>',
        '<li>elem3<span class="float-right">29</span></li>',
        '<li>elem4<span class="float-right">29</span></li>',
        '<li>elem5<span class="float-right">29</span></li>',
        '<li>elem6<span class="float-right">29</span></li>',
        '<li>elem7<span class="float-right">29</span></li>',
        '<li>elem8<span class="float-right">29</span></li>',
        '<li>elem9<span class="float-right">29</span></li>',
        '<li>elem10<span class="float-right">29</span></li>',
    ]}
        elementsPerPage=4
    />

{:else}

<ul class="mb-4">
    {#each elements.slice(parseInt(currentPage * elementsPerPage), parseInt(currentPage * elementsPerPage) + parseInt(elementsPerPage)) as elem, i}

    {@html elem}

    {/each}
</ul>

<div class="w-full flex justify-center">
    <NumberButtonGroup bind:active={currentPage} bind:pageNums={pageNums} />
</div>


{/if}