<script>
    import { getUniqueValueFromArray } from "../lib/array.js";
    import Modal from "../modals/Modal.svelte";

    export let tabNames = ["My Account", "Company", "Team Members", "Billing"];
    export let selectedIdx = 0;
    export let inputValue = tabNames[selectedIdx];
    export let breakpoint = "md";
    export let includeDelete = true;
    export let deleteText = 'Delete Tab'

    let select;

    let activeTab;

    let showingDeleteModal = false;

    $: tabNames[selectedIdx] = inputValue;

    function addTab() {
        let name = getUniqueValueFromArray(tabNames, "Untitled");
        tabNames.push(name);
        inputValue = name;
        selectedIdx = tabNames.length - 1;
    }

    function getUniqueValue(value) {
        // make reference free temp array
        let temp = JSON.parse(JSON.stringify(tabNames));
        delete temp[select.selectedIndex];
        return getUniqueValueFromArray(temp, value);
    }
</script>

<!-- No purge section -->
<!--
sm:block
md:block
lg:block
sm:hidden
md:hidden
lg:hidden
-->

<div>
    <div class="{breakpoint}:hidden">
        <label for="tabs" class="sr-only">Select a tab</label>
        <!-- Use an "onChange" listener to redirect the user to the selected tab URL. -->
        <select
            bind:this={select}
            on:change={() => {
                inputValue = getUniqueValue(select.value);
                selectedIdx = select.selectedIndex;
            }}
            class="block w-full pl-3 pr-10 py-2 text-base border border-gray-300 dark:border-gray-800 bg-inherit dark:text-primary-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md">
            {#each tabNames as tabName, i}
                <option class="dark:bg-slate-900 bg-slate-50" selected={i == selectedIdx}>{tabName}</option>
            {/each}
        </select>
        <button on:click={addTab} class=""> + Add New </button>
        <input
            class="px-4 bg-4 w-fit"
            bind:value={inputValue}
            on:keydown={(e) => (e.code == "Enter" ? e.preventDefault() : "")}
            on:input={() => {
                inputValue = getUniqueValue(inputValue);
            }} />
    </div>
    <div class="hidden {breakpoint}:block">
        <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-8 overflow-x-auto" aria-label="Tabs">
                <!-- Current: "border-primary-500 text-primary-600", Default: "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300" -->
                {#each tabNames as tabName, i}
                    {#if selectedIdx == i}
                        <button
                            bind:this={activeTab}
                            contenteditable="true"
                            on:keydown={(e) => (e.code == "Enter" ? e.preventDefault() : "")}
                            on:input={() => {
                                inputValue = getUniqueValue(activeTab.innerText);
                            }}
                            class="dark:border-primary-300 dark:text-primary-400 border-primary-500 text-primary-600 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm focus-visible:outline-none cursor-text"
                            aria-current="page">{tabName}</button>
                    {:else}
                        <button
                            on:click={() => {
                                inputValue = tabName;
                                selectedIdx = i;
                            }}
                            class="border-transparent text-gray-500 dark:hover:text-gray-300 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
                            >{tabName}</button>
                    {/if}
                {/each}
                <button
                    class="border-transparent text-gray-500  hover:text-gray-700 hover:border-gray-300 whitespace-nowrap dark:hover:text-gray-300 py-4 px-1 border-b-2 font-medium text-sm"
                    on:click={addTab}>
                    +
                </button>
            </nav>
        </div>
    </div>
</div>

<div class="flex justify-center mt-4 w-full">
    <div class="">
        {inputValue}
    </div>
    {#if includeDelete}
        <button
            class="justify-self-end border-transparent rounded-md whitespace-nowrap py-2 px-4 border-b-2 font-medium text-sm bg-red-500 text-red-200 hover:text-red-300"
            on:click={() => (showingDeleteModal = true)}>
            {deleteText}
        </button>
    {/if}
</div>

<Modal bind:open={showingDeleteModal}>
    <!-- This example requires Tailwind CSS v2.0+ -->
    <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
            <div class="mt-2 max-w-xl text-sm text-gray-500">
                <p>Are you sure you want to delete team <span class="font-extrabold">{inputValue}?</p>
            </div>
            <div class="flex justify-end mt-5">
                <button
                    on:click={() => showingDeleteModal = false}
                    class="text-sm text-gray-400 mr-4">Cancel</button>
                <button
                    type="button"
                    on:click={() => {
                        tabNames.splice(selectedIdx, 1);
                        tabNames = [...tabNames];
                        selectedIdx = selectedIdx - 1;
                        inputValue = tabNames[selectedIdx];
                        showingDeleteModal = false;
                    }}
                    class="inline-flex items-center justify-center px-4 py-2 border border-transparent font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:text-sm"
                    >Delete</button>
            </div>
        </div>
    </div>
</Modal>
