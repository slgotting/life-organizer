<script>
  import { onMount } from "svelte";
  import { slide } from 'svelte/transition';
  import { spring } from "svelte/motion";

  export let folderName = "";
  export let treeObject = {};
  export let depth = 0;

  export let textColorOne = 'text-primary-300'
  export let textColorTwo = 'text-green-200'

//   let files = treeObject.files;
//   delete treeObject.files;
//   let directories = treeObject;

    let files = [];
    let directories = {}

    for (let [key, value] of Object.entries(treeObject)) {
        if (key == 'files') {
            files = value;
        } else {
            directories[key] = value;
        }
    }

  let open = false;

  if (depth == 0) {
    open = true;
  }

  $: logFiles(open);

  function logFiles(open) {
      console.log(files);
      console.log(directories);
  }

</script>

{#if folderName.length > 0}
  <li
    class="flex ml-auto px-2 py-2
    border-gray-400
    dark:border-gray-800
    dark:bg-gray-700
    cursor-pointer border-t
    dark:text-primary-300
    text-primary-500
    {(depth==1) ? 'border-r dark:border-r-0' : 'border-l'}
    "
    style={depth == 1 ? '' : 'width:93%'}
    on:click={() => (open = !open)}>
    {folderName.toUpperCase()}
    <span class="ml-auto">
        <svg xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6 transform {open ? 'rotate-180' : ''}
            transition duration-300"
            fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
    </span>
</li>
{/if}

{#if open}
<ul transition:slide|local
  class="flex-col overflow-hidden
  dark:border-gray-800
  dark:bg-gray-600
  ml-auto
  dark:text-white
  text-gray-600
  border-gray-400
  {(depth==1) ? 'border-r dark:border-r-0' : 'border-l'}
  "
  style={depth <= 1 ? '' : 'width:93%'}>

  {#each files as file}
    <li class="px-2 pr-6 py-1 cursor-pointer">{file}</li>
  {/each}

  {#each Object.keys(directories) as directory}
    <svelte:self
      folderName={directory}
      treeObject={directories[directory]}
      depth={depth + 1} />
  {/each}
</ul>

{/if}
