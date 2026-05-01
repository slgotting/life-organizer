<script>
    import BodyBackdrop from "../backdrops/BodyBackdrop.svelte";
    import { fly } from "svelte/transition";
    import DocumentBackdrop from "../backdrops/DocumentBackdrop.svelte";
    import { onMount } from "svelte";

    export let open = false;
    export let center = false;

    export let modalPosition = "body";

    let modal;

    function appendToBody() {
        let body = document.getElementsByTagName("body");
        console.log(body);
        document.getElementsByTagName("body")[0].appendChild(modal);
    }

    function openModal() {
        open = true;
        calculateCenter();
        appendToBody();
    }

    let position;
    function calculateCenter() {
        let width = window.screen.width;
        let height = window.screen.height;

        // console.log(modal.offsetHeight);

        let pos;
    }

    function positionModal(open) {
        if (open) {
            calculateCenter();
        }
    }

    $: positionModal(open);
</script>

{#if open}
<div
    bind:this={modal}
    in:fly|local={{ y: -30, duration: 500 }}
    out:fly|local={{ y: -30, duration: 500 }}
    class="modal absolute z-50 shadow-8"
    style={position}>
    <slot />
</div>
{/if}

            <!-- {open ? 'block' : 'hidden'} -->
<!-- backdrop -->
<DocumentBackdrop bind:visible={open} />

<!-- {/if} -->
<style>
    .perfect-center {
        position: absolute;
        transform: translate(-50%, -50%);
        left: 50%;
        top: 50%;
    }

    /* .modal {
        opacity: 0;

        will-change: transform, opacity;
        transform: scale(1.15);

        transition: transform 0.1s cubic-bezier(0.465, 0.183, 0.153, 0.946), opacity 0.1s cubic-bezier(0.465, 0.183, 0.153, 0.946);
    }
    .modal.block {
        pointer-events: auto;
        opacity: 1;
        transform: scale(1);

        transition: transform 0.3s cubic-bezier(0.465, 0.183, 0.153, 0.946), opacity 0.3s cubic-bezier(0.465, 0.183, 0.153, 0.946);
    } */
</style>
