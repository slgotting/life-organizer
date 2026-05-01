<script>
  // enter items as {'href': ..., 'name': ...}
  export let items = [];
</script>

<style>

</style>

<ul class="flex">
  {#each items as item}
    <a href={item.href}>
      <li class="px-2 text-primary dark:text-red-300">{item.name}</li>
    </a>
  {/each}
</ul>
