<script>
    import Vime from './Vime.svelte';
    import BaseModal from '../../modals/BaseModal.svelte';

    export let example = false;

    export let buttonText = "Open Video"
    export let source = "/static/video/test.mp4";
    export let poster = "";

    export let width = "sm:w-[75vw] w-screen"

    export let modal;
    export let open;


    export let btnClass = "flex justify-center w-full py-3 px-4 rounded-md shadow bg-gradient-to-r from-primary-500 to-primary-600 text-white font-medium hover:from-primary-600 hover:to-primary-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-400 focus:ring-offset-gray-900";

    $: visible = open

</script>

{#if example}

    <svelte:self />

{:else}


    <button class="{btnClass}" on:click={() => modal.openModal()}>{ buttonText }</button>
    <BaseModal bind:this={modal} bind:open={open} >
        <div class="{width} border-4 rounded-lg {open ? 'block': 'hidden'}">
            <Vime {poster} {source} />
        </div>
    </BaseModal>

{/if}