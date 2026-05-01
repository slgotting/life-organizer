<script>
    import * as easing from 'svelte/easing';
    export let href = "#";
    export let name = "Projects";
    export let shouldScroll = true;
    export let scrollDuration = 1500;
</script>

{#if shouldScroll}
<a {href}
    class="w-16 h-24 relative">
    <div id="header" class="w-full text-center box py-8" style="top:-10%;">
    { name }
    </div>
    <div class="box h-fit w-fit">
        <span />
        <span />
        <span />
    </div>
</a>
{:else}
<a {href} on:click={(e) => e.preventDefault()} class="w-16 h-24 relative cursor-default">
    <div id="header" class="w-full text-center box py-8 cursor-default" style="top:-10%;">
    { name }
    </div>
    <div class="box h-fit w-fit">
        <span />
        <span />
        <span />
    </div>
</a>
{/if}


<style>
    .box {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        pointer-events: none;
    }

    .dark .box span {
        border-bottom: 2px solid white;
        border-right: 2px solid white;
    }
    .box span {
        border-bottom: 2px solid black;
        border-right: 2px solid black;
    }

    .box span {
        pointer-events: none;
        display: block;
        width: 20px;
        height: 20px;
        transform: rotate(45deg);
        margin: -10px;
        animation: animate 2s infinite;
    }

    .box span:nth-child(2) {
        animation-delay: -0.2s;
    }

    .box span:nth-child(3) {
        animation-delay: -0.4s;
    }


    @keyframes animate {
        0% {
            opacity: 0;
            transform: rotate(45deg) translate(-20px, -20px);
        }
        50% {
            opacity: 1;
        }
        100% {
            opacity: 0;
            transform: rotate(45deg) translate(20px, 20px);
        }
    }
</style>
