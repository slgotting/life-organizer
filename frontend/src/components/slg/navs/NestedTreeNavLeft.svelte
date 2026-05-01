<script>
  // nav that is either the width on the left or has a menu button at the top to expose
  // it on mobile
  // accordion style nav with tabs and sub components

  // IMPORTANT: In order to use with a builtin body, wrap your content with the NestedTreeNavLeftWrapper instead
  import { onMount } from "svelte";
  import NestedAccordion from "../accordions/NestedAccordion.svelte";

  // tree structure is {'files': [...files], 'directory1': {...treeObj}, 'directoryN': {...treeObj}}
  export let treeObject = {};

  // using tailwind specs for different screen sizes
  export let width = "w-0 md:w-60 xl:w-72";
  let smallScreen;

  export let baseColor = "gray";
  export let baseStrength = "600";

  let open = false;

  let openTab = "";

  function isScreenSmall(cutoff = 768) {
    return window.outerWidth < cutoff;
  }

  onMount(async () => {
    smallScreen = isScreenSmall();

    document.addEventListener("resize", () => {
      // check is screen is small
      smallScreen = isScreenSmall();
    });
  });
</script>

<style>

</style>

<button
  class="md:hidden flex {open ? 'w-screen' : 'w-24'} h-8 items-center
  justify-center bg-gray-700 rounded-r z-40"
  on:click={() => (open = !open)}>
  {open ? 'Close' : 'Menu ->'}
</button>

<div class="{open && smallScreen ? 'w-screen' : width} z-20 sh-1
            border-b border-gray-400 dark:border-gray-800">
  <ul class="border-{baseColor}-{baseStrength}">
    <NestedAccordion {treeObject} />
  </ul>
</div>
