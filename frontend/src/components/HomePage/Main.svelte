
<script>
    import Loader from "../slg/loaders/Loader.svelte";

    let loading = false;
</script>

{#if loading}
    <div class="fixed left-0 top-0 w-screen h-screen z-40 bg-gray-900/80 pointer-events-none">
        <div class="absolute top-1/3 left-1/2 -translate-x-1/2 m-0">
            <div class="w-12">
                <Loader />
            </div>
        </div>
    </div>
{:else}
    <div>Logged in!</div>
{/if}