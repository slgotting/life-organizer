<script>
    import { slide, fade, scale, draw, crossfade, blur, fly } from "svelte/transition";

    import { cubicOut } from "svelte/easing";
    import { onMount } from 'svelte'
    import VideoModal from '../../media/video/VideoModal.svelte';
    import LinkNewTab from '../../links/LinkNewTab.svelte';

    export let offset = 100;
    export let animationParamsLeft = { x: -100, duration: 1000, easing: cubicOut }
    export let animationParamsRight = { x: 100, duration: 1000, easing: cubicOut }

    export let imgSrc = `https://tailwindui.com/img/ecommerce-images/product-feature-07-detail-01.jpg`
    export let imgAlt = imgSrc;

    export let examples = [
        // {
        //     'description': 'Component',
        //     'source': '/static/gifs/ff-analysis-1.gif'
        // },
        // {
        //     'description': 'End to End',
        //     'source': '/static/gifs/ff-analysis-1.gif'
        // },
    ];

    export let id = "";

    export let transition = "fly";

    export let descriptionSide = "right";


    export let hideUntilVisible = "true";

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
            visible = true
        }
    }


    function getScrollY() {
        return window.scrollY
    }


    let scrollY;
    $: showElem(scrollY)

    onMount(() => {
        setTimeout(() => { // small timeout to allow all page loading to occur
            yPosition = topRef.getBoundingClientRect().top;

            showElem(getScrollY())

        }, 200);
    })
</script>

<svelte:window bind:scrollY={scrollY} bind:innerHeight={windowHeight} />


{#if descriptionSide == 'left'}


<div {id} bind:this={topRef}>
    {#if visible}
        <div bind:this={elem} class="flex lg:grid flex-col-reverse lg:grid-cols-12 lg:gap-x-8 lg:items-center">
            <div in:fly|local={animationParamsLeft} class="mt-6 lg:mt-0 lg:row-start-1 lg:col-span-5 xl:col-span-4 lg:col-start-1">

                <slot name="information">

                    <h3 class="text-lg font-medium text-gray-900 dark:text-gray-50">
                        Minimal and thoughtful
                    </h3>
                    <p class="mt-2 text-sm text-gray-500">
                        Our laptop sleeve is compact and precisely fits 13&quot; devices. The zipper allows you to access the interior with ease, and the front
                        pouch provides a convenient place for your charger cable.
                    </p>

                </slot>

            </div>
            <div in:fly|local={animationParamsRight} class="flex-auto lg:row-start-1 lg:col-span-7 xl:col-span-8 lg:col-start-6 xl:col-start-5">

                <div class="aspect-w-5 aspect-h-2 rounded-lg overflow-hidden bg-slate-700 shadow-12">

                    <img
                        src="{ imgSrc }"
                        alt="{ imgAlt }"
                        class="object-center object-cover" />
                </div>

                {#if examples.length > 0}
                    <div class="flex flex-col sm:flex-row justify-center items-center mt-4">
                        <div class="text-sm mr-4 mb-4 sm:mb-0 ml-4">
                            Demos:
                        </div>
                        <div class="flex justify-center items-center divide-x">
                            {#each examples as example}
                                <div class="px-4 text-primary-500 hover:text-primary-600 dark:text-primary-400 hover:dark:text-primary-300 sm:text-sm text-sm">
                                    <VideoModal buttonText="{ example.description }" source="{ example.source }" />
                                </div>
                                <!-- /home/steven/Videos/FF-Analysis/CreateGameDefinition.mp4
                                /home/steven/Videos/FF-Analysis/EndToEnd.mp4 -->
                            {/each}
                        </div>
                    </div>
                {/if}

            </div>


        </div>
    {:else}
        <div bind:this={elem} class="invisible flex lg:grid flex-col-reverse lg:grid-cols-12 lg:gap-x-8 lg:items-center">
            <div class="mt-6 lg:mt-0 lg:row-start-1 lg:col-span-5 xl:col-span-4 lg:col-start-1">

                <slot name="information">

                    <h3 class="text-lg font-medium text-gray-900 dark:text-gray-50">
                        Minimal and thoughtful
                    </h3>
                    <p class="mt-2 text-sm text-gray-500">
                        Our laptop sleeve is compact and precisely fits 13&quot; devices. The zipper allows you to access the interior with ease, and the front
                        pouch provides a convenient place for your charger cable.
                    </p>

                </slot>

            </div>
            <div class="flex-auto lg:row-start-1 lg:col-span-7 xl:col-span-8 lg:col-start-6 xl:col-start-5">
                <div class="aspect-w-5 aspect-h-2 rounded-lg bg-gray-100 overflow-hidden">
                    <img
                        src="{ imgSrc }"
                        alt="{ imgAlt }"
                        class="object-center object-cover" />
                </div>

                {#if examples.length > 0}
                    <div class="flex flex-col sm:flex-row justify-center items-center mt-4">
                        <div class="text-sm mr-4 mb-4 sm:mb-0 ml-4">
                            Demos:
                        </div>
                        <div class="flex justify-center items-center divide-x">
                            {#each examples as example}
                                <div class="px-4 text-primary-500 hover:text-primary-600 dark:text-primary-400 hover:dark:text-primary-300 sm:text-sm text-sm">
                                    <VideoModal buttonText="{ example.description }" source="{ example.source }" />
                                </div>
                                <!-- /home/steven/Videos/FF-Analysis/CreateGameDefinition.mp4
                                /home/steven/Videos/FF-Analysis/EndToEnd.mp4 -->
                            {/each}
                        </div>
                    </div>
                {/if}

            </div>
        </div>
    {/if}
</div>


{:else if descriptionSide == 'right'}

<div {id} bind:this={topRef}>
    {#if visible}
        <div bind:this={elem} class="flex lg:grid flex-col-reverse lg:grid-cols-12 lg:gap-x-8 lg:items-center">
            <div in:fly|local={animationParamsRight}
                class="mt-6 lg:mt-0 lg:row-start-1 lg:col-span-5 xl:col-span-4 lg:col-start-8 xl:col-start-9">

                <slot name="information">

                    <h3 class="text-lg font-medium text-gray-900 dark:text-gray-50">
                        Minimal and thoughtful
                    </h3>
                    <p class="mt-2 text-sm text-gray-500">
                        Our laptop sleeve is compact and precisely fits 13&quot; devices. The zipper allows you to access the interior with ease, and the front
                        pouch provides a convenient place for your charger cable.
                    </p>

                </slot>

            </div>
            <div
                in:fly|local={animationParamsLeft}
                class="flex-auto lg:row-start-1 lg:col-span-7 xl:col-span-8 lg:col-start-1">

                <div class="aspect-w-5 aspect-h-2 rounded-lg shadow-12 overflow-hidden">

                    <img
                        src="{ imgSrc }"
                        alt="{ imgAlt }"
                        class="object-center object-cover" />
                </div>


                {#if examples.length > 0}
                    <div class="flex flex-col sm:flex-row justify-center items-center mt-4">
                        <div class="text-sm mr-4 mb-4 sm:mb-0 ml-4">
                            Demos:
                        </div>
                        <div class="flex justify-center items-center divide-x">
                            {#each examples as example}
                                <div class="px-4 text-primary-500 hover:text-primary-600 dark:text-primary-400 hover:dark:text-primary-300 sm:text-sm text-sm">
                                    <VideoModal buttonText="{ example.description }" source="{ example.source }" />
                                </div>
                                <!-- /home/steven/Videos/FF-Analysis/CreateGameDefinition.mp4
                                /home/steven/Videos/FF-Analysis/EndToEnd.mp4 -->
                            {/each}
                        </div>
                    </div>
                {/if}


            </div>
        </div>

    {:else}
        <div bind:this={elem} class="invisible flex lg:grid flex-col-reverse lg:grid-cols-12 lg:gap-x-8 lg:items-center">
            <div
                class="mt-6 lg:mt-0 lg:row-start-1 lg:col-span-5 xl:col-span-4 lg:col-start-8 xl:col-start-9">

                <slot name="information">

                    <h3 class="text-lg font-medium text-gray-900 dark:text-gray-50">
                        Minimal and thoughtful
                    </h3>
                    <p class="mt-2 text-sm text-gray-500">
                        Our laptop sleeve is compact and precisely fits 13&quot; devices. The zipper allows you to access the interior with ease, and the front
                        pouch provides a convenient place for your charger cable.
                    </p>

                </slot>

            </div>
            <div class="flex-auto lg:row-start-1 lg:col-span-7 xl:col-span-8 lg:col-start-1">
                <div class="aspect-w-5 aspect-h-2 rounded-lg overflow-hidden">
                    <img
                        src="{ imgSrc }"
                        alt="{ imgAlt }"
                        class="object-center object-cover" />
                </div>

                {#if examples.length > 0}
                    <div class="flex flex-col sm:flex-row justify-center items-center mt-4">
                        <div class="text-sm mr-4 mb-4 sm:mb-0 ml-4">
                            Demos:
                        </div>
                        <div class="flex justify-center items-center divide-x">
                            {#each examples as example}
                                <div class="px-4 text-primary-500 hover:text-primary-600 dark:text-primary-400 hover:dark:text-primary-300 sm:text-sm text-sm">
                                    <VideoModal buttonText="{ example.description }" source="{ example.source }" />
                                </div>
                                <!-- /home/steven/Videos/FF-Analysis/CreateGameDefinition.mp4
                                /home/steven/Videos/FF-Analysis/EndToEnd.mp4 -->
                            {/each}
                        </div>
                    </div>
                {/if}


            </div>
        </div>
    {/if}
</div>
{/if}
