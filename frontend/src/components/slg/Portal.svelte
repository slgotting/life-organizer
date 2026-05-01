<script>
  // src/components/Portal.svelte
  import { onMount, onDestroy } from "svelte";
  let ref;
  let portal;

  onMount(async () => {
    portal = document.createElement("div");
    portal.className = "portal";
    document.body.appendChild(portal);
    portal.appendChild(ref);
  });

  onDestroy(() => {
    document.body.removeChild(portal);
  });
</script>

<style>
  .portal-clone {
    display: none;
  }
</style>

<div class="portal-clone">
  <div bind:this={ref}>
    <slot />
  </div>
</div>


<!-- Ok so this portal takes an element and basically appends it to the body for absolute positioning.
    Its useful for things that need to be positioned relative to the body.
-->