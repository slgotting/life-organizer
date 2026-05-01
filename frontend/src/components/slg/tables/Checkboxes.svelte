<script>

export let title = "Users";
export let description = "A list of all the users in your account including their name, title, email and role."
export let example = false;
export let rowClickCallback;

export let headers = [
    'Name',
    'Title',
    'Email',
    'Role',
]

export let rows = [
    {
        'name': 'Lindsay Walton',
        'title': 'Front-end Developer',
        'email': 'lindsay.walton@example.com',
        'role': 'Member',
    },
    {
        'name': 'Lindsay Walton',
        'title': 'Front-end Developer',
        'email': 'lindsay.walton@example.com',
        'role': 'Member',
    }
]

export let selectedRows = [];

let allChecked = false;

function range(min, max, step=1) {
    let output = [];
    for (let i=min; i<max; i+=step) {
        output.push(i);
    }
    return output;
}

function toggleSelected(idx) {
    if (selectedRows.includes(idx)) {
        selectedRows.splice(selectedRows.indexOf(idx),1);
        selectedRows = [...selectedRows];
    } else {
        selectedRows = [...selectedRows, idx];
    }
}

function toggleSelectAll(checked) {
    if (checked) {
        selectedRows = range(0, rows.length);
    } else {
        selectedRows = [];
    }
}

function convertValueToTableValue(row, field) {
    let value = row[field] || row[field.toLowerCase()] || ''
    if (typeof value == 'boolean') {
        return (value) ? `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
  <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
</svg>` : `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
</svg>
`
    } else {
        return value;
    }
}

$: toggleSelectAll(allChecked);

</script>

<!--
  This example requires some changes to your config:

  ```
  // tailwind.config.js
  module.exports = {
    // ...
    plugins: [
      // ...
      require('@tailwindcss/forms'),
    ],
  }
  ```
-->
{#if example}
    <svelte:self />
{:else}
<div class="px-4 sm:px-6 lg:px-8 max-w-full">
  <div class="sm:flex sm:items-center">
  {#if title || description}
    <div class="sm:flex-auto">
      <h1 class="text-base font-semibold leading-6 text-daw-gray-900">{title}</h1>
      <p class="mt-2 text-daw-gray-700">{description}</p>
    </div>
    {/if}
  </div>
  <div class="{title || description ? "mt-8" : "mt-2"} flow-root">
    <div class="overflow-x-auto">
      <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
        <div class="relative">
          <!-- Selected row actions, only show when rows are selected. -->
          <!-- <div class="absolute top-0 left-14 flex h-12 items-center space-x-3 bg-white sm:left-12"> -->
          <!--   <button type="button" class="inline-flex items-center rounded bg-white px-2 py-1 font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:bg-white">Bulk edit</button> -->
          <!--   <button type="button" class="inline-flex items-center rounded bg-white px-2 py-1 font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:bg-white">Delete all</button> -->
          <!-- </div> -->

          <table class="min-w-full table-fixed divide-y divide-daw-gray-300">
            <thead>
              <tr>
                <th scope="col" class="relative px-7 sm:w-12 sm:px-6">
                  <input type="checkbox" bind:checked={allChecked} class="absolute left-4 top-1/2 -mt-2 h-4 w-4 rounded border-daw-gray-300 text-primary-600 focus:ring-primary-600">
                </th>
                {#each headers as header}
                <th scope="col" class="px-3 py-3.5 text-left font-semibold text-daw-gray-900">{header}</th>
                {/each}
              </tr>
            </thead>
            <tbody class="divide-y divide-daw-gray-200">
              <!-- Selected: "bg-gray-50" -->
            {#each rows as row, i}
              <tr class="{rowClickCallback ? 'cursor-pointer' : ''}">
                <td class="relative px-7 sm:w-12 sm:px-6">
                  <input type="checkbox" on:change={() => toggleSelected(i)} checked={selectedRows.includes(i)} class="absolute left-4 top-1/2 -mt-2 h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-600">
                </td>
                {#each headers as field}
                <!-- <td class="whitespace-nowrap py-4 pr-3 font-medium text-daw-gray-900">{row.name || ''}</td> -->
                <td class="whitespace-nowrap px-3 py-4 text-daw-gray-600"  on:click={(e) => rowClickCallback(e, row)}>
                    {#if typeof row[field] === 'boolean' || typeof row[field.toLowerCase()] === 'boolean'}
                        {#if row[field] === true || row[field.toLowerCase()] === true}
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                            </svg>
                        {:else}
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                            </svg>
                        {/if}
                    {:else}
                        {row[field] || row[field.toLowerCase()] || ''}
                    {/if}
                </td>
                {/each}
              </tr>
            {/each}

            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</div>

{/if}