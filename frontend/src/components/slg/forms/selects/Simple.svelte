<script>
    import { fly } from 'svelte/transition';
    import Button from '../../primitives/Button.svelte';
    export let label = "Assigned to";
    export let options = ['Tom Cook', 'Wade Coop', 'Cooper Kupp'];
    export let open = false;
    export let labelClasses = "block text-sm font-medium text-gray-700 dark:text-gray-200"
    export let buttonClasses = "bg-inherit relative w-full border dark:border-gray-700 border-gray-300 dark:text-gray-50 text-gray-800 rounded-md shadow-sm pl-3 pr-10 py-2 text-left cursor-default focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
    export let dropdownClasses = "absolute z-20 mt-1 w-full bg-1 dark:bg-gray-800 bg-white text-gray-800 dark:text-gray-50 shadow-lg max-h-60 rounded-md text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm border-4 border-daw-gray-100"
    export let disabled = false;

    export let value;

    if (!value) {
        value = options[0];
    }

    let selectDropdown;

    // remove pointer events if phasing out
    function removePointerEvents(elem) {
        elem.style.pointerEvents = 'none';
    }

    // add pointer events if phasing in
    function addPointerEvents(elem) {
        elem.style.pointerEvents = 'all';
    }

</script>

<!-- This example requires Tailwind CSS v2.0+ -->
<div>
    {#if label}
        <label class={labelClasses}>{label}</label>
    {/if}
    <div class="relative">
        <button
            disabled={disabled}
            type="button"
            on:click={() => (open = !open)}
            class={buttonClasses}
            aria-haspopup="listbox"
            aria-expanded="true"
            aria-labelledby="listbox-label">
            <span class="block truncate">{value}</span>
            <span class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                <!-- Heroicon name: solid/selector -->
                <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path
                        fill-rule="evenodd"
                        d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                        clip-rule="evenodd" />
                </svg>
            </span>
        </button>

        <!--
        Select popover, show/hide based on select state.

        Entering: ""
          From: ""
          To: ""
        Leaving: "transition ease-in duration-100"
          From: "opacity-100"
          To: "opacity-0"
      -->
        {#if open}
            <ul
                bind:this={selectDropdown}
                on:outrostart={removePointerEvents(selectDropdown)}
                on:introstart={addPointerEvents(selectDropdown)}
                in:fly|local={{x:-20, duration:500}}
                out:fly|local={{x:-20, duration:500}}
                class={dropdownClasses}
                tabindex="-1"
                role="listbox"
                aria-labelledby="listbox-label"
                aria-activedescendant="listbox-option-3">
                <!--
          Select option, manage highlight styles based on mouseenter/mouseleave and keyboard navigation.

          Highlighted: "text-white bg-indigo-600", Not Highlighted: "text-gray-900"
        -->
            {#each options as option, i}
                <li
                    on:click={() => {
                        value = option;
                        // selectedIdx = i;
                        open = false;
                    }}
                    class="cursor-default select-none relative py-2 pl-3 pr-9 hover:bg-primary-600 hover:text-white
                            {option == value ? 'dark:text-primary-400 text-primary-600 hover:dark:text-white' : 'text-gray-900 dark:text-gray-50'}"
                    id="listbox-option-0"
                    role="option">
                    <!-- selectedIdx: "font-semibold", Not selectedIdx: "font-normal" -->
                    <span class="font-normal block truncate">{option}</span>

                    <!--
            Checkmark, only display for selectedIdx option.

            Highlighted: "text-white", Not Highlighted: "text-indigo-600"
          -->
                    <!-- {#if selectedIdx == i} -->
                    {#if option == value}
                    <span class="text-current absolute inset-y-0 right-0 flex items-center pr-4">
                        <!-- Heroicon name: solid/check -->
                        <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path
                                fill-rule="evenodd"
                                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                clip-rule="evenodd" />
                        </svg>
                    </span>
                    {/if}
                </li>
            {/each}
                <!-- More items... -->
            </ul>

            <div
                class="fixed left-0 top-0 w-screen h-screen z-10"
                on:click={() => open = false}
            />
        {/if}
    </div>
</div>
