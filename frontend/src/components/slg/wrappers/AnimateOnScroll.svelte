<script>
    import AOSLibrary from 'aos';

    AOSLibrary.init({
        offset: 0,
    });

    export let animation="fade-up"
    export let offset="200"
    export let delay="50"
    export let duration="1000"
    export let easing="ease-out-cubic"
    export let mirror="true"
    export let once="false"
    export let anchorPlacement="top-center"

    export let example = false;

</script>

{#if example}

    <div class="h-96">

    </div>

    <svelte:self offset="-300" once="true">
        <button class="px-4 py-12 bg-gray-400">Hey</button>
        <button class="px-4 py-12 bg-gray-400">Hey</button>
        <button class="px-4 py-12 bg-gray-400">Hey</button>
        <button class="px-4 py-12 bg-gray-400">Hey</button>
        <button class="px-4 py-12 bg-gray-400">Hey</button>
    </svelte:self>

{:else}

<div
    data-aos="{animation}"
    data-aos-offset="{offset}"
    data-aos-delay="{delay}"
    data-aos-duration="{duration}"
    data-aos-easing="{easing}"
    data-aos-mirror="{mirror}"
    data-aos-once="{once}"
    data-aos-anchor-placement="{anchorPlacement}"
  >
<slot />
</div>

{/if}