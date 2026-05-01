<script>
    import NavTop from "../navs/hero/Top.svelte";
    import * as easing from 'svelte/easing';
    import * as animateScroll from 'svelte-scrollto';

    export let logo = "https://tailwindui.com/img/logos/workflow-mark-indigo-600.svg"
    export let headerText1 = 'Data to enrich your'
    export let headerText2 = 'small business'
    export let descriptionText = 'Anim aute id magna aliqua ad ad non deserunt sunt. Qui irure qui lorem cupidatat commodo. Elit sunt amet fugiat veniam occaecat fugiat aliqua.'

    export let button1 = {'href': '#', 'name': 'Get started'}
    export let button2 = {'href': '#', 'name': 'Live demo'}

    export let scrollDuration = 1500;

    export let navObjects = [
        { href: "#", name: "Dashboard" },
        { href: "#", name: "Team" },
        { href: "#", name: "Projects" },
        { href: "#", name: "Calendar" },
    ];

    // Nav Options
    export let includeLogo = true;
    export let includeDarkToggle = true;

    export let rightSide = "contact"; // contact,login
    export let rightSideHref = "#contact";
</script>

<!-- This example requires Tailwind CSS v2.0+ -->
<div class="relative overflow-hidden">
    <div class="hidden sm:block sm:absolute sm:inset-y-0 sm:h-full sm:w-full" aria-hidden="true">
        <div class="relative h-full max-w-7xl mx-auto">
            <svg
                class="absolute right-full transform translate-y-1/4 translate-x-1/4 lg:translate-x-1/2"
                width="404"
                height="784"
                fill="none"
                viewBox="0 0 404 784">
                <defs>
                    <pattern id="f210dbf6-a58d-4871-961e-36d5016a0f49" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
                        <rect x="0" y="0" width="4" height="4" class="dark:text-gray-800 text-gray-200" style="transition" fill="currentColor" />
                    </pattern>
                </defs>
                <rect width="404" height="784" fill="url(#f210dbf6-a58d-4871-961e-36d5016a0f49)" />
            </svg>
            <svg
                class="absolute left-full transform -translate-y-3/4 -translate-x-1/4 md:-translate-y-1/2 lg:-translate-x-1/2"
                width="404"
                height="784"
                fill="none"
                viewBox="0 0 404 784">
                <defs>
                    <pattern id="5d0dd344-b041-4d26-bec4-8d33ea57ec9b" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
                        <rect x="0" y="0" width="4" height="4" class="dark:text-gray-800 text-gray-200" fill="currentColor" />
                    </pattern>
                </defs>
                <rect width="404" height="784" fill="url(#5d0dd344-b041-4d26-bec4-8d33ea57ec9b)" />
            </svg>
        </div>
    </div>

    <div class="relative pt-6 pb-16 sm:pb-24">
        <div>
            <NavTop
                {logo}
                {navObjects}
                {rightSide}
                {rightSideHref}
            />
        </div>
        <main class="mt-16 mx-auto max-w-7xl px-4 sm:mt-24">
            <div class="text-center">
                <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 dark:text-gray-50 sm:text-5xl md:text-6xl">
                    <span class="block xl:inline">{headerText1}</span>
                    <span class="block text-primary-600 xl:inline">{headerText2}</span>
                </h1>
                <p class="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
                    {descriptionText}
                </p>
                <div class="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
                    <div class="rounded-md shadow">
                        <a
                            href="{button1.href}"
                            on:click|preventDefault={() => animateScroll.scrollTo({element: button1.href, offset: -100,  duration: scrollDuration, easing: easing.cubicOut })}
                            class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 md:py-4 md:text-lg md:px-10">
                            {button1.name}
                        </a>
                    </div>
                    <div class="mt-3 rounded-md shadow sm:mt-0 sm:ml-3">
                        <a
                            href="{button2.href}"
                            on:click|preventDefault={() => animateScroll.scrollTo({element: button2.href, offset: -100,  duration: scrollDuration, easing: easing.cubicOut })}
                            class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-primary-600 bg-white hover:bg-gray-50 hover:dark:bg-gray-200 md:py-4 md:text-lg md:px-10">
                            {button2.name}
                        </a>
                    </div>
                </div>
            </div>
        </main>
    </div>
</div>