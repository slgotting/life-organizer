<script>
    import { slide, fade, scale, draw, crossfade, blur, fly } from 'svelte/transition';
    export let configLocation = '';
    import navObjects from "../../../../config/navs.js";
    import { logoSvg, logoPng } from "../../../../config/logo.js";
    import { siteTitle } from "../../../../config/general.js";

    import VideoModal from '../../media/video/VideoModal.svelte';
    // let navObjects = import(`${configLocation}/navs.js`);


    export let navigationObjects = navObjects;
    export let brandSvg = logoSvg || 'https://tailwindui.com/img/logos/workflow-mark-primary-500-secondary-600.svg';
    export let brandPng = logoPng || 'https://tailwindui.com/img/logos/workflow-mark-primary-500-secondary-600.svg';
    export let header1 = 'A better way to'
    export let header2 = 'ship web apps'
    export let description = 'Anim aute id magna aliqua ad ad non deserunt sunt. Qui irure qui Lorem cupidatat commodo. Elit sunt amet fugiat veniam occaecat fugiat.'

    export let img = 'https://tailwindui.com/img/component-images/cloud-illustration-indigo-400.svg'

    export let navRightObjects = {

    }

    let mobileNavVisible = false;

</script>

<!--
require('@tailwindcss/forms'),
require('@tailwindcss/aspect-ratio'),
 -->

<div class="bg-1">
    <div class="relative overflow-hidden">
        <header class="relative">
            <div class="bg-1 pt-6">
                <nav class="relative max-w-7xl mx-auto flex items-center justify-between px-4 sm:px-6" aria-label="Global">
                    <div class="flex items-center flex-1">
                        <div class="flex items-center justify-between w-full md:w-auto">
                            <a href="#">
                                <span class="sr-only">{ siteTitle }</span>
                                <img class="h-8 w-auto sm:h-10" src="{ brandSvg }" alt="" />
                            </a>
                            <div class="-mr-2 flex items-center md:hidden">
                                <button
                                    on:click={() => mobileNavVisible = true}
                                    type="button"
                                    class="bg-gray-900 rounded-md p-2 inline-flex items-center justify-center text-gray-400 hover:bg-gray-800 focus:outline-none focus:ring-2 focus-ring-inset focus:ring-white"
                                    aria-expanded="false">
                                    <span class="sr-only">Open main menu</span>
                                    <!-- Heroicon name: outline/menu -->
                                    <svg
                                        class="h-6 w-6"
                                        xmlns="http://www.w3.org/2000/svg"
                                        fill="none"
                                        viewBox="0 0 24 24"
                                        stroke="currentColor"
                                        aria-hidden="true">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                                    </svg>
                                </button>
                            </div>
                        </div>
                        <div class="hidden space-x-8 md:flex md:ml-10">
                            {#each navObjects as obj}
                            <a href="{obj.href}" class="text-base font-medium text-white hover:text-gray-300">{ obj.name } </a>
                            {/each}
                        </div>
                    </div>
                    <div class="hidden md:flex md:items-center md:space-x-6">
                        <a href="#" class="text-base font-medium text-white hover:text-gray-300"> Log in </a>
                        <a
                            href="#"
                            class="inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md text-white bg-gray-600 hover:bg-gray-700">
                            Start free trial
                        </a>
                    </div>
                </nav>
            </div>

            <!--
          Mobile menu, show/hide based on menu open state.

          Entering: "duration-150 ease-out"
            From: "opacity-0 scale-95"
            To: "opacity-100 scale-100"
          Leaving: "duration-100 ease-in"
            From: "opacity-100 scale-100"
            To: "opacity-0 scale-95"
        -->
        {#if mobileNavVisible}
            <div
                in:fly|local={{ x: -100, duration: 500}}
                out:fly|local={{ x: -100, duration: 500}}
                class="absolute top-0 inset-x-0 p-2 transition transform origin-top md:hidden">
                <div class="rounded-lg shadow-md bg-2 ring-1 ring-black ring-opacity-5 overflow-hidden">
                    <div class="px-5 pt-4 flex items-center justify-between">
                        <div>
                            <a href="/">
                                <img class="h-8 w-auto" src="{ brandPng }" alt="" />
                            </a>
                        </div>
                        <div class="-mr-2">
                            <button
                                on:click={() => mobileNavVisible = false}
                                type="button"
                                class="rounded-md p-2 inline-flex items-center justify-center text-gray-400 hover:bg-gray-100 hover:dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-600">
                                <span class="sr-only">Close menu</span>
                                <!-- Heroicon name: outline/x -->
                                <svg
                                    class="h-6 w-6"
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                    aria-hidden="true">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                        </div>
                    </div>
                    <div class="pt-5 pb-6">
                        <div class="px-2 space-y-1">
                            {#each navObjects as obj}
                                <a href="{obj.href}" class="block px-3 py-2 rounded-md text-base font-medium  hover:bg-gray-50 hover:dark:bg-gray-900">{obj.name}</a>
                            {/each}
                        </div>
                        <!-- <div class="mt-6 px-5">
                            <a
                                href="#"
                                class="block text-center w-full py-3 px-4 rounded-md shadow bg-gradient-to-r from-primary-500 to-primary-600 text-white font-medium hover:from-primary-600 hover:to-secondary-700"
                                >Start free trial</a>
                        </div>
                        <div class="mt-6 px-5">
                            <p class="text-center text-base font-medium text-gray-500">
                                Existing customer? <a href="#" class="text-gray-900 hover:underline">Login</a>
                            </p>
                        </div> -->
                    </div>
                </div>
            </div>
        {/if}
        </header>
        <main>
            <div class="pt-10 bg-1 sm:pt-16 lg:pt-8 lg:pb-14 lg:overflow-hidden">
                <div class="mx-auto max-w-7xl lg:px-8">
                    <div class="lg:grid lg:grid-cols-2 lg:gap-8">
                        <div class="mx-auto max-w-md px-4 sm:max-w-2xl sm:px-6 sm:text-center lg:px-0 lg:text-left lg:flex lg:items-center">
                            <div class="lg:py-24">
                                <!-- <a
                                    href="#"
                                    class="inline-flex items-center text-white bg-black rounded-full p-1 pr-2 sm:text-base lg:text-sm xl:text-base hover:text-gray-200">
                                    <span
                                        class="px-3 py-0.5 text-white text-sm font-semibold leading-5 uppercase tracking-wide bg-gradient-to-r from-primary-500 to-primary-600 rounded-full"
                                        >We're hiring</span>
                                    <span class="ml-4 text-sm">Visit our careers page</span>

                                    <svg
                                        class="ml-2 w-5 h-5 text-gray-500"
                                        xmlns="http://www.w3.org/2000/svg"
                                        viewBox="0 0 20 20"
                                        fill="currentColor"
                                        aria-hidden="true">
                                        <path
                                            fill-rule="evenodd"
                                            d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                                            clip-rule="evenodd" />
                                    </svg>
                                </a> -->
                                <h1 class="mt-4 text-4xl tracking-tight font-extrabold text-white sm:mt-5 sm:text-6xl lg:mt-6 xl:text-6xl">
                                    <span class="block">{ header1 }</span>
                                    <span class="pb-3 block bg-clip-text text-transparent bg-gradient-to-r from-primary-200 to-primary-400 sm:pb-5"
                                        >{ header2 }</span>
                                </h1>
                                <p class="text-base text-gray-300 sm:text-xl lg:text-lg xl:text-xl">
                                    {@html description }
                                </p>
                                <div class="mt-10 sm:mt-12">
                                    <div class="sm:max-w-xl sm:mx-auto lg:mx-0">
                                        <div class="sm:flex">
                                            <div class="min-w-0 flex-1">
                                                <a href="/usage">
                                                    <button
                                                        type="submit"
                                                        class="block w-full py-3 px-4 rounded-md shadow bg-gradient-to-r from-primary-500 to-primary-600 text-white font-medium hover:from-primary-600 hover:to-primary-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-400 focus:ring-offset-gray-900"
                                                        >Get Started</button>
                                                </a>
                                            </div>
                                            <div class="mt-3 sm:mt-0 sm:ml-3">
                                                <VideoModal buttonText="See Demo" source="static/video/TimeLog-EndToEnd.mp4" />
                                                <!-- <button
                                                    type="submit"

                                                    class="block w-full py-3 px-4 rounded-md shadow bg-gradient-to-r from-primary-500 to-primary-600 text-white font-medium hover:from-primary-600 hover:to-primary-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-400 focus:ring-offset-gray-900"
                                                    >See Demo</button> -->
                                            </div>
                                        </div>
                                        <!-- <p class="mt-3 text-sm text-gray-300 sm:mt-4">
                                            Start your free 14-day trial, no credit card necessary. By providing your email, you agree to our <a
                                                href="#"
                                                class="font-medium text-white">terms of service</a
                                            >.
                                        </p> -->
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="mt-12 -mb-16 sm:-mb-48 lg:m-0 lg:relative">
                            <div class="mx-auto max-w-md px-4 sm:max-w-2xl sm:px-6 lg:max-w-none lg:px-0">
                                <!-- Illustration taken from Lucid Illustrations: https://lucid.pixsellz.io/ -->
                                <img
                                    class="w-full lg:absolute lg:inset-y-0 lg:left-0 lg:h-full lg:w-auto lg:max-w-none"
                                    src="{ img }"
                                    alt="" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</div>