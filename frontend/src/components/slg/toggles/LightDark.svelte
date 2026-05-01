<script>
    import { fade, fly } from "svelte/transition";
    import { onMount } from "svelte";

    export let condensed = false;
    export let moonColorStrength1 = 600;
    export let moonColorStrength2 = 400;

    export let borderColor = "border-primary-500"

    // if dark mode is enabled in the <html> tag's class with class="dark" then change this to true,
    // else false. For some reason checking the document element onMount and changing it dynamically
    // doesn't do anything
    let darkMode = localStorage.getItem('darkMode');
    if (darkMode == null) {
        darkMode = true;
    }
    if (darkMode == 'false') {
        console.log('removing dark class');
        document.querySelector('html').classList.remove('dark');
    }

    // leave this here to remember than instead, we will apply the dark class to the <html> tag in
    // app.html.
    //   onMount(async () => {
    //     // toggleDarkMode(darkMode);
    //   });

    let moonColor1;
    let moonColor2;
    function setMoonColors(darkMode) {
        moonColor1 = getComputedStyle(document.querySelector(`.text-primary-${moonColorStrength1}`)).color;
        moonColor2 = getComputedStyle(document.querySelector(`.text-primary-${moonColorStrength2}`)).color;
    }

    function toggleDarkMode() {
        darkMode = !darkMode;
        if (darkMode) {
            document.documentElement.classList.add("dark");
        } else {
            document.documentElement.classList.remove("dark");
        }
    }

    onMount(async () => {
        if (!document.documentElement.classList.contains("dark")) {
            darkMode = false;
        }
        setMoonColors();
    });

    $: localStorage.setItem('darkMode', darkMode);
</script>


{#if condensed}
    <button
        class="relative h-8"
        on:click={toggleDarkMode}
    >
    {#if darkMode}
        <div
            id="moon"
            class="absolute perfect-center"
            in:fly|local={{ y: -10, duration: 600 }}
            out:fly|local={{ y: -10, duration: 600 }}
        >
            <svg
                class="w-8 h-8"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 64 64"
            >
                <circle cx="32" cy="32" r="30" fill="{moonColor1}" />
                <g fill="{moonColor2}">
                    <circle cx="50" cy="35.2" r="7" />
                    <circle cx="18.1" cy="39" r="6" />
                    <circle cx="24.2" cy="50" r="9" />
                    <circle cx="24" cy="17.2" r="4" />
                    <circle cx="37" cy="18.2" r="4" />
                    <circle cx="12.1" cy="25.9" r="4" />
                    <circle cx="39" cy="9.2" r="2" />
                    <circle cx="8.1" cy="39" r="2" />
                    <circle cx="52" cy="50" r="2" />
                    <circle cx="25" cy="29.9" r="3" />
                    <circle cx="15" cy="15.7" r="2" />
                    <circle cx="46" cy="52.6" r="4" />
                    <path
                        d="M24.2 10.8c0 2.8 2.2 5 5 5s5-2.2 5-5-2.2-5-5-5c-2.8-.1-5 2.2-5 5"
                    />
                </g>
            </svg>
        </div>
    {:else}
        <div
        id="sun"
        class="absolute perfect-center"
        in:fly|local={{ y: 10, duration: 600 }}
        out:fly|local={{ y: 10, duration: 600 }}
    >
        <svg
            class="w-12 h-8 transform"
            style="transform: rotate(180deg) scaleY(-1);"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            viewBox="0 0 512 512"
            enable-background="new 0 0 512 512"
            xml:space="preserve"
        >
            <g id="Layer_2">
                <circle
                    fill="#FFD60D"
                    cx="102.865"
                    cy="203.064"
                    r="98.903"
                />
            </g>
            <g id="Layer_3">
                <path
                    fill="#B0E9FF"
                    d="M441.518,309.419c-5.51,0-10.859,0.682-15.98,1.945c1.143-4.982,1.767-10.161,1.767-15.489
        c0-38.123-30.905-69.028-69.028-69.028c-14.467,0-27.889,4.459-38.983,12.065c-12.949-49.89-58.284-86.729-112.225-86.729
        c-64.031,0-115.939,51.908-115.939,115.939c-48.141,0-87.168,39.026-87.168,87.168c0,48.141,39.026,87.168,87.168,87.168h350.388
        c36.738,0,66.52-29.782,66.52-66.52C508.038,339.201,478.256,309.419,441.518,309.419z"
                />
            </g>
        </svg>
    </div>
    {/if}

    </button>
{:else}
<button
    class="
    relative w-20 h-8 rounded-2xl border shadow-sm
    cursor-pointer
    {borderColor}"
    on:click={toggleDarkMode}
>
    {#if darkMode}
        <div
            id="moon"
            class="absolute"
            style="top:3px; left:6px;"
            in:fly|local={{ x: 30, duration: 1000 }}
            out:fly|local={{ x: 30, duration: 1000 }}
        >
            <svg
                class="w-6 h-6"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 64 64"
            >
                <circle cx="32" cy="32" r="30" fill="{moonColor1}" />
                <g fill="{moonColor2}">
                    <circle cx="50" cy="35.2" r="7" />
                    <circle cx="18.1" cy="39" r="6" />
                    <circle cx="24.2" cy="50" r="9" />
                    <circle cx="24" cy="17.2" r="4" />
                    <circle cx="37" cy="18.2" r="4" />
                    <circle cx="12.1" cy="25.9" r="4" />
                    <circle cx="39" cy="9.2" r="2" />
                    <circle cx="8.1" cy="39" r="2" />
                    <circle cx="52" cy="50" r="2" />
                    <circle cx="25" cy="29.9" r="3" />
                    <circle cx="15" cy="15.7" r="2" />
                    <circle cx="46" cy="52.6" r="4" />
                    <path
                        d="M24.2 10.8c0 2.8 2.2 5 5 5s5-2.2 5-5-2.2-5-5-5c-2.8-.1-5 2.2-5 5"
                    />
                </g>
            </svg>
        </div>
    {:else}
        <div
            id="sun"
            class="absolute right-0"
            style="top: -2px;"
            in:fly|local={{ x: -30, duration: 1000 }}
            out:fly|local={{ x: -30, duration: 1000 }}
        >
            <svg
                class="w-12 h-8 transform"
                style="transform: rotate(180deg) scaleY(-1);"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink"
                viewBox="0 0 512 512"
                enable-background="new 0 0 512 512"
                xml:space="preserve"
            >
                <g id="Layer_2">
                    <circle
                        fill="#FFD60D"
                        cx="102.865"
                        cy="203.064"
                        r="98.903"
                    />
                </g>
                <g id="Layer_3">
                    <path
                        fill="#B0E9FF"
                        d="M441.518,309.419c-5.51,0-10.859,0.682-15.98,1.945c1.143-4.982,1.767-10.161,1.767-15.489
            c0-38.123-30.905-69.028-69.028-69.028c-14.467,0-27.889,4.459-38.983,12.065c-12.949-49.89-58.284-86.729-112.225-86.729
            c-64.031,0-115.939,51.908-115.939,115.939c-48.141,0-87.168,39.026-87.168,87.168c0,48.141,39.026,87.168,87.168,87.168h350.388
            c36.738,0,66.52-29.782,66.52-66.52C508.038,339.201,478.256,309.419,441.518,309.419z"
                    />
                </g>
            </svg>
        </div>
    {/if}
</button>
{/if}


<style>
    .perfect-center {
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
    }
</style>