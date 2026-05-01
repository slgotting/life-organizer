<script>
    import { fade } from "svelte/transition";
  import Portal from "../Portal.svelte";
  export let visible = false;

  export let fadeDuration = 500;
</script>


<!-- This portal enables the usage of modals. I forgot to document exactly how -->
<Portal>
  <div id="backdrop"
    transition:fade|local={{duration: fadeDuration}}
    class="fixed left-0 top-0 w-screen h-screen z-40"
    class:hidden={!visible}
    on:click={() => (visible = false)} />
</Portal>

<style>
    #backdrop {
        background-color: rgba(0,0,0, 0.4);
    }
</style>