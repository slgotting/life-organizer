<script>
    import { onMount } from "svelte";
    import Loader from "../loaders/Loader.svelte";

    let button;

    export let example = false;

    export let disabled = false;
    export let componentType = "basic"; // basic

    export let loaderStyle = "flex items-center justify-center";
    export let loading = false;
    export let loaderSize = "size-4"

    export let buttonType = "button" // button,submit,reset

    export let size = "md"

    export let classes = "inline-flex items-center px-3 py-2 font-medium shadow-sm text-white focus:outline-none focus:ring-2 focus:ring-offset-2 bg-primary-600 hover:bg-primary-700 focus:ring-primary-500 disabled:bg-daw-gray-300"

    const SIZE_MAP = {
        'unset': '',
        'xs': 'px-2.5 py-1.5 text-sm rounded',
        'sm': 'px-3 py-2 text-sm leading-4 rounded-md',
        'md': 'px-4 py-2 text-sm rounded-md',
        'lg': 'px-4 py-2 text-base rounded-md',
        'xl': 'px-6 py-3 text-base rounded-md',
    }

    let computedWidth, computedHeight;
    onMount(() => {
        const style = window.getComputedStyle(button);
        computedWidth = style.width;
        computedHeight = style.height;
    })
</script>

{#if example}

    <svelte:self size="md">
        Example Button
    </svelte:self>

{:else}

    <button
        bind:this={button}
        {disabled}
        on:click
        type={buttonType}
        class="{SIZE_MAP[size]} {classes}"
        style="width: {computedWidth}; height: {computedHeight};"
        >
        {#if loading}
        <div class="{loaderStyle}">
            <Loader size={loaderSize} />
        </div>
        {:else}
        <slot />
        {/if}
    </button>

{/if}
