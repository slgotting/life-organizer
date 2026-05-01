<script>
    import { slide, fade, scale, draw, crossfade, blur, fly } from "svelte/transition";

    import { cubicOut } from "svelte/easing";

    import { onMount } from "svelte";

    export let id = "";

    export let offset = 100;

    export let animationParamsLeft = { x: -500, duration: 2000, easing: cubicOut }
    export let animationParamsRight = { x: -500, duration: 2000, easing: cubicOut }


    let visible = false;
    let elem;
    let yPosition;
    let windowHeight;
    let topRef;

    // let yPos = getYPosition();
    // function getYPosition() {
    //     elem.offsetH
    // }

    // function scrolledIntoView

    // function scrollCheck(scroll) {
    //     if scroll
    // }

    // if (hideUntilVisible) {
    //     if (window.
    // } else {
    //     visible = true;
    // }

    function showElem(scrollY) {
        if (windowHeight + scrollY > yPosition + offset) {
            visible = true;
        }
    }

    let scrollY;
    $: showElem(scrollY);

    onMount(() => {
        setTimeout(() => {
            // small timeout to allow all page loading to occur
            yPosition = topRef.getBoundingClientRect().top;
        }, 200);
    });
</script>

<svelte:window bind:scrollY bind:innerHeight={windowHeight} />


<div {id} bind:this={topRef}>
    {#if visible}
        <div bind:this={elem} class="flex lg:grid flex-col-reverse lg:grid-cols-12 lg:gap-x-8 lg:items-center">
            <div in:fly|local={animationParamsRight}
                class="mt-6 lg:mt-0 lg:row-start-1 lg:col-span-5 xl:col-span-4 lg:col-start-8 xl:col-start-9">
                <h3 class="text-lg font-medium text-gray-900">Refined details</h3>
                <p class="mt-2 text-sm text-gray-500">
                    We design every detail with the best materials and finishes. This laptop sleeve features durable canvas with double-stitched construction, a
                    felt interior, and a high quality zipper that hold up to daily use.
                </p>
            </div>
            <div
                in:fly|local={animationParamsLeft}
                class="flex-auto lg:row-start-1 lg:col-span-7 xl:col-span-8 lg:col-start-1">
                <div class="aspect-w-5 aspect-h-2 rounded-lg bg-gray-100 overflow-hidden">
                    <img
                        src="https://tailwindui.com/img/ecommerce-images/product-feature-07-detail-02.jpg"
                        alt="Detail of zipper pull with tan leather and silver rivet."
                        class="object-center object-cover" />
                </div>
            </div>
        </div>

    {:else}
        <div bind:this={elem} class="invisible flex-col-reverse lg:grid-cols-12 lg:gap-x-8 lg:items-center">
            <div
                class="mt-6 lg:mt-0 lg:row-start-1 lg:col-span-5 xl:col-span-4 lg:col-start-8 xl:col-start-9">
                <h3 class="text-lg font-medium text-gray-900">Refined details</h3>
                <p class="mt-2 text-sm text-gray-500">
                    We design every detail with the best materials and finishes. This laptop sleeve features durable canvas with double-stitched construction, a
                    felt interior, and a high quality zipper that hold up to daily use.
                </p>
            </div>
            <div class="flex-auto lg:row-start-1 lg:col-span-7 xl:col-span-8 lg:col-start-1">
                <div class="aspect-w-5 aspect-h-2 rounded-lg bg-gray-100 overflow-hidden">
                    <img
                        src="https://tailwindui.com/img/ecommerce-images/product-feature-07-detail-02.jpg"
                        alt="Detail of zipper pull with tan leather and silver rivet."
                        class="object-center object-cover" />
                </div>
            </div>
        </div>
    {/if}
</div>
