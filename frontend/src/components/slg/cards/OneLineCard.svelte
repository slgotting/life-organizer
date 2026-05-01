<script>
  let shrinkToFit = true;
</script>

<style>
  .shrinkToFit {
    width: fit-content;
  }
</style>

<div class="px-2 py-4 shadow-md rounded-sm text-sm" class:shrinkToFit>
  <slot />
</div>
