<script>
    // nav that is either the width on the left or has a menu button at the top to expose
    // it on mobile
    // accordion style nav with tabs and sub components

    // IMPORTANT: wrap this in a flex-col container with the body content in order to use

    // key name (of outer label) to a list of components
    export let accordionTabs = {}

    export let fontSize = "1rem";
    export let textColor = "white";

    // using tailwind specs for different screen sizes
    export let width = "w-0 md:w-60 xl:w-72";

    export let baseColor = 'gray';
    export let baseStrength = '600';


    let open = false;

    let openTab = '';

</script>

<style>

</style>

<button class="md:hidden flex {open ? 'w-screen' : 'w-24' } h-8 items-center justify-center bg-gray-700 rounded-r z-40" on:click={() => open = !open}>
    {open ? 'X' : 'Menu ->'}
</button>

<nav class="{open ? 'w-screen' : width} h-screen z-40 overflow-hidden shadow-lg">
    <ul class="border-t-2 border-{baseColor}-{baseStrength}">


        {#each Object.keys(accordionTabs) as tab}
            <li class="px-4 py-2 text-center border-r-2 border-{baseColor}-{baseStrength} bg-{baseColor}-{baseStrength - 100} cursor-pointer"
                on:click={() => {
                    openTab = (openTab == tab) ? '' : tab;
                }}
                >{tab}<span class="float-right pr-6">{openTab == tab ? '/\\': '\\/'}</span></li>
            <ul class="flex-col text-right {(openTab == tab) ? 'h-auto' : 'h-0'} overflow-hidden bg-{baseColor}-{baseStrength - 200} border-b-2 border-r-2 border-{baseColor}-{baseStrength}">
                {#each accordionTabs[tab] as component}
                    <li class="px-2 pr-6 py-1 cursor-pointer">{component}</li>
                {/each}
            </ul>
        {/each}
    </ul>
</nav>
