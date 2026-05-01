<script>
    import DefineCategory from "./DefineCategory.svelte";
    import { addKeyValueToStorage, getKeyFromStorage } from '../../lib/storage.js';
    import Delete from "../../confirmation/Delete.svelte";
    import Info from "../../informative/Info.svelte";
    import { slide, fade, scale, draw, crossfade, blur, fly } from "svelte/transition";
    import { getFirstUniqueId } from '../../lib/array.js';
    import { playSound } from '../../lib/sounds.js';
    import {flip} from 'svelte/animate';


    import { getUniqueValueFromArray } from "../../lib/array.js";

    export let title = "Category Definitions";
    export let confirmDelete = true;
    export let confirmDeletePosition = 'middle-center';
    export let tooltipPos = 'top';
    export let tooltip = `
    <div class="text-sm">A <i class="text-lg mx-2">Category Definition</i> is defined as the set of rules that define a category. Currently the only boolean operation supported is "OR" so
        that means if a rule matches, it is classified as that category.
    </div>
    `
    let deleteModalOpen = false;
    let deleteCategorySound;

    let hovering;

    export let whereToAddNewCategoryGroups = "front"

    export let defaultRule = (id) => {
        return {
            id: id,
            options: ['String', 'Regex'],
            selectedOption: 'String',
            value: "StringToMatch",
        }
    }
    export let defaultCategory = {
        name: "Untitled",
        id: 0,
        collapsed: false,
        rules: [
            defaultRule(1)
        ]
    }

    export let categoryDefinitions = [JSON.parse(JSON.stringify(defaultCategory))];

    categoryDefinitions = getKeyFromStorage({key: "categoryDefinitions"}) || categoryDefinitions;

    function addCategory(where = "front") {
        let categoryNames = categoryDefinitions.map((el) => el.name);
        let newName = getUniqueValueFromArray(categoryNames, 'Untitled');
        let newId = getFirstUniqueId(categoryDefinitions);
        if (where == "front") {
            categoryDefinitions = [{id: newId, name: newName, rules: [defaultRule(1)]}, ...categoryDefinitions]
        } else {
            categoryDefinitions = [...categoryDefinitions, {id: newId, name: newName, rules: [defaultRule(1)]}]
        }
    }

    let idxToDelete = 0;
    function deleteCategory(idx) {
        categoryDefinitions.splice(idx, 1);
        categoryDefinitions = [...categoryDefinitions];

        playSound(deleteCategorySound)
    }

    function getCategoryName(idx) {
        try {
            return categoryDefinitions[idxToDelete].name
        } catch {}
    }

    function moveDownOne(i) {
        categoryDefinitions = arrayMove(categoryDefinitions, i, i+1)
    }

    function moveUpOne(i) {
        categoryDefinitions = arrayMove(categoryDefinitions, i, i-1)
    }
    function arrayMove(arr, old_index, new_index) {
        if (new_index >= arr.length || new_index < 0) {
            return arr;
        }
        if (new_index >= arr.length) {
            var k = new_index - arr.length + 1;
            while (k--) {
                arr.push(undefined);
            }
        }
        arr.splice(new_index, 0, arr.splice(old_index, 1)[0]);
        return arr; // for testing
    };


    $: addKeyValueToStorage({key: "categoryDefinitions", value: categoryDefinitions});

</script>

<div class="flex justify-center mb-2">
    <h2 class="text-3xl text-center my-2">{title}</h2>
{#if tooltip}
<Info {tooltipPos}>
    <div in:fade|local={{duration: 400}} class="dark:bg-slate-800 bg-white px-4 py-2 rounded-md max-w-xs shadow-4">
        {@html tooltip}
    </div>
</Info>
{/if}
</div>


<div class="w-full flex justify-evenly mb-8">
    <button on:click={() => addCategory(whereToAddNewCategoryGroups)} class="dark:text-green-400 text-sm hover:text-green-500 text-green-600">
        Add Category +
    </button>
    <div class="text-sm">
        <button on:click={() => {
            let hiddenDefinitions = categoryDefinitions.map(el => {
                el.collapsed = true;
                return el;
            })
            categoryDefinitions = hiddenDefinitions;
        }}
            class="dark:text-secondary-300 text-secondary-700">
            Hide
        </button>
        <span class="mx-1 ">/</span>
        <button on:click={() => {
            let shownDefinitions = categoryDefinitions.map(el => {
                el.collapsed = false;
                return el;
            })
            categoryDefinitions = shownDefinitions;
        }}
            class="dark:text-secondary-300 text-secondary-700">
            Show
        </button>
        <span class="ml-2">All</span>
    </div>
</div>

{#if confirmDelete}

<Delete position={confirmDeletePosition} bind:open={deleteModalOpen} deleteCallback={() => deleteCategory(idxToDelete)}>
    <div slot="title">Delete Category</div>
    <div slot="description">Are you sure you want to delete category <i>{getCategoryName(idxToDelete)}</i>?</div>
</Delete>

{/if}

{#each categoryDefinitions as category, i (category.id)}

    <div
        in:fly|local={{y:-50, duration:500}}
        out:fly|local={{x:20, duration:100}}
        animate:flip|local
    >

    {#if confirmDelete}

        <DefineCategory bind:category={categoryDefinitions[i]} storageKey={''} > <!-- storageKey is null because we are handling storage in this component -->
            <div slot="deleteAndChangePosBtns" class="flex relative top-1 left-[-50px] pr-4">
                <div class="text-sm font-extrabold text-red-400 hover:text-red-500 cursor-pointer relative top-2"
                    on:click={() => {
                        idxToDelete = i;
                        deleteModalOpen = true;
                    }}>
                    X
                </div>
                <div class="flex flex-col ml-4">
                    <div class="cursor-pointer"
                        on:click={() => moveUpOne(i)}
                        >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                        </svg>
                    </div>
                    <div class="cursor-pointer"
                        on:click={() => moveDownOne(i)}
                        >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                        </svg>
                    </div>
                </div>
            </div>
        </DefineCategory>
    {:else}

        <DefineCategory bind:category={categoryDefinitions[i]} storageKey={''} > <!-- storageKey is null because we are handling storage in this component -->
            <div class="text-sm font-extrabold text-red-400 hover:text-red-500 cursor-pointer top-2 relative" slot="delete" on:click={() => deleteCategory(i)}>
                X
            </div>
        </DefineCategory>
    {/if}

    </div>
{/each}


<audio
    bind:this={deleteCategorySound}
    src="/static/sounds/paper_file.wav"
></audio>