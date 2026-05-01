
<script>
  import { page } from '$app/stores';
</script>

{#if $page.status == '404'}
<div class="grid min-h-full place-items-center px-6 py-24 sm:py-32 lg:px-8">
  <div class="text-center">
    <p class="text-base font-semibold text-daw-primary-600">404</p>
    <h1 class="mt-4 text-3xl font-bold tracking-tight text-daw-gray-900 sm:text-5xl">Page not found</h1>
    <p class="mt-6 text-base leading-7 text-daw-gray-600">Sorry, we couldn’t find the page you’re looking for.</p>
    <div class="mt-10 flex items-center justify-center gap-x-6">
      <a href="/" class="rounded-md bg-daw-primary-600 px-3.5 py-2.5 text-sm font-semibold text-daw-white shadow-sm hover:bg-daw-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Go back home</a>
    </div>
  </div>
</div>

{:else}
<h1>{$page.status}: {$page.error.message}</h1>
{/if}