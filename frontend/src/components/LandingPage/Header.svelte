<!-- @format -->
<script>
    import Info from "../slg/informative/Info.svelte";
    import { fly } from "svelte/transition";
    import DescriptionWithArrowTRtoBl from "../slg/handdrawn/DescriptionWithArrowTRtoBL.svelte";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher()
</script>

<div class="relative isolate px-6 pt-14 lg:px-8">
    <div class="mx-auto max-w-2xl">
        <!-- <div class="hidden sm:mb-8 sm:flex sm:justify-center">
        <div class="relative rounded-full px-3 py-1 text-sm leading-6 text-daw-gray-600 ring-1 ring-gray-900/10 hover:ring-gray-900/20">
          Announcing our next round of funding. <a href="#" class="font-semibold text-daw-blue-700"><span class="absolute inset-0" aria-hidden="true"></span>Read more <span aria-hidden="true">&rarr;</span></a>
        </div>
      </div> -->
        <div class="relative text-center">

            <!-- <img class="hidden sm:block absolute perfect-center w-48  -mt-12 lg:w-96 lg:mt-24 -z-20" src="images/cards3.png" alt=""> -->

            <!-- <h1 class="text-4xl font-bold tracking-tight text-daw-gray-900 sm:text-6xl">Flux Flashcards</h1> -->
            <div class="mt-6 flex flex-col items-center leading-8 text-daw-gray-900">
                <div class="flex flex-col items-center font-extrabold tracking-tight text-4xl sm:text-6xl">
                    <div class="z-20">
                    Do a certain thing, with
                    </div>
                    <div class="relative w-fit -top-2">
                        <div class="bg-blue-500 rotate-6 z-10
                            w-fit text-center items-center px-3 py-2 tracking-tight
                            font-extrabold shadow-sm text-white focus:outline-none focus:ring-2 focus:ring-offset-2
                            bg-gradient-to-r to-blue-400 from-blue-500 focus:ring-blue-500
                        ">
                            <div class="-rotate-6">
                                steeze[n]
                            </div>
                        </div>
                        <div class="absolute top-2 -right-2">
                        <Info size={"w-6 h-6"}>
                            <div
                                in:fly|local={{ duration: 400, y: 20 }}
                                class="w-36 dark:bg-slate-600 bg-white px-4 py-2 rounded-md max-w-xs shadow-xl">
                                <div class="text-sm font-medium tracking-wide text-daw-gray-800">Applying "flux" is our way of saying the question and answer have been modified by AI</div>
                            </div>
                        </Info>
                        </div>
                    </div>
                </div>
                <!-- <div>
                    Boost retention and generalized understanding. Fill in the gaps of understanding by automatically generating new questions,
                    one's you may have never even thought of asking.
                </div> -->

                <!-- <div class="w-80">
                    Coupling spaced-repetition with fluctuating questions provides the necessary leverage to break down the most complex of topics
                </div> -->
                <!-- <div class="w-80 text-gray-400 text-md leading-6"> -->
                <div class="mt-2 max-w-2xl text-balance leading-normal text-muted-foreground text-md sm:text-lg text-gray-400">
                    Gain the leverage necessary to break down complex topics by coupling spaced-repetition with perpetual fluctuation
                </div>
            </div>
            <div class="mt-10 flex items-center justify-center gap-x-6">
                <a
                    href="signup"
                    class="rounded-md bg-white px-3.5 py-2.5 text-sm text-daw-gray-100 shadow-sm hover:bg-gray-200 border-2"
                    >Get started</a>
                <div class="relative">
                    <button class="button-home"
                        on:click={() => dispatch('startDemo')} >
                        Demo
                    </button>
                        <!-- <div class="sm:hidden absolute top-32 left-24">
                            <DescriptionWithArrowTRtoBl>
                                <div class="relative -right-10 top-28 text-white text-sm w-12" style="font-family: handwritten; text-shadow: 1px 1px 4px black;">
                                    Try it out!
                                </div>
                            </DescriptionWithArrowTRtoBl>
                        </div> -->
                        <div class="absolute -right-12 -top-24">
                            <DescriptionWithArrowTRtoBl>
                                <div class="relative -right-12 top-24 text-white text-sm w-12" style="font-family: handwritten;">
                                    Try it out!
                                </div>
                            </DescriptionWithArrowTRtoBl>
                        </div>
                </div>
            </div>
        </div>
    </div>
    <div
        class="absolute inset-x-0 top-[calc(100%-13rem)] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[calc(100%-30rem)] pointer-events-none"
        aria-hidden="true">
        <div
            class="relative left-[calc(50%+3rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%+36rem)] sm:w-[72.1875rem]"
            style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)">
        </div>
    </div>


</div>
