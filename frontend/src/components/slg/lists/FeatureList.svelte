<script>

    export let example = false;

    export let features = [
        {
            'id': 0,
            'title': 'Invite team members',
            'description': 'You can manage phone, email and chat conversations all from a single mailbox.',
        },
        {
            'id': 1,
            'title': 'Notifications',
            'description': 'Find what you need with advanced filters, bulk actions, and quick views.',
        },
        {
            'id': 2,
            'title': 'Calendars',
            'description': 'You can manage phone, email and chat conversations all from a single mailbox.',
        },
    ];

</script>

{#if example}

    <svelte:self />

{:else}



<!-- This example requires Tailwind CSS v2.0+ -->

      <!-- <div class="mt-12 lg:mt-0 lg:col-span-2">
        <div class="space-y-10 sm:space-y-0 sm:grid {rows} {cols} sm:grid-flow-col sm:gap-x-6 sm:gap-y-10 lg:gap-x-8"> -->
    <div class="space-y-10">
        {#each features as feature, i (feature.id)}
          <div class="relative">
            <div>
              <!-- Heroicon name: outline/check -->
              <svg class="absolute h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <p class="ml-9 text-lg leading-6 font-medium text-gray-900 dark:text-gray-50">{ feature.title }</p>
            </div>
            <dd class="mt-2 ml-9 text-base text-gray-500">{ feature.description }</dd>
          </div>
        {/each}
        </div>
        <!-- </div>
      </div> -->


{/if}