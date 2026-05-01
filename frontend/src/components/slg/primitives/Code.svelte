<script>
    import { slide, fade, scale, draw, crossfade, blur, fly } from 'svelte/transition';
    import { copyElemText } from "../lib/clipboard.js";

    export let example = false;

    export let bg = "bg-gray-300 dark:bg-gray-800";
    export let componentType = "Linux"; // Linux

    let code;

    let showingCopied = false;
    function showCopied() {
        showingCopied = true
        setTimeout(() => {
            showingCopied = false
        }, 5);
    }
</script>

{#if example}
    <svelte:self />
{:else}
    <div class="flex flex-col w-fit">
        <div class="flex w-fit {bg} px-4 py-2 rounded-md">
            <span class="text-gray-400 dark:text-gray-700 pointer-events-none select-none"> $ </span>
            <div bind:this={code} class="ml-2 tracking-wide">
                <slot />
            </div>
            <button class="ml-6 cursor-pointer relative"
                on:click={() => {
                    copyElemText(code);
                    showCopied();
                }}
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 dark:text-gray-700 text-gray-400 hover:dark:text-white hover:text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                </svg>
                {#if showingCopied}
                    <div
                        out:fly={{ y:-25, duration:1000}}
                        class="absolute top-[-12px] left-[-12px] text-sm">
                        Copied!
                    </div>
                {/if}
            </button>
        </div>
    </div>
{/if}
