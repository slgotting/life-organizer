<script>
    import SelectInputCombo from "../combinations/SelectInputCombo.svelte";
    import { addKeyValueToStorage, getKeyFromStorage } from '../../lib/storage.js';
    import { getFirstUniqueId } from '../../lib/array.js';
    import { playSound } from '../../lib/sounds.js';
    import { slide, fade, scale, draw, crossfade, blur, fly } from "svelte/transition";

    let deleteCategorySound;
    let hovering = false;

    export let defaultRule = (id) => {
        return {
            id: id,
            options: ['String', 'Regex'],
            selectedOption: 'String',
            value: "StringToMatch",
        }
    }
    export let defaultCategory = {
        name: "Work",
        collapsed: false,
        rules: [
            defaultRule(1)
        ]
    }

    export let addNewDefinitionsWhere = 'back';
    export let storageKey = 'category'
    export let category;

    if (storageKey) {
        category = getKeyFromStorage({key: storageKey}) || JSON.parse(JSON.stringify(defaultCategory));
    }

    $: addKeyValueToStorageLocal(category)

    function addKeyValueToStorageLocal(category) {
        if (storageKey) {
            addKeyValueToStorage({
                key: storageKey,
                value: category
            })
        }
    }

    function addRule() {
        let newId = getFirstUniqueId(category.rules);
        if (addNewDefinitionsWhere == 'front') {
            category.rules = [JSON.parse(JSON.stringify(defaultRule(newId))), ...category.rules];
            // rules = [defaultCategory].concat([...rules]);
        } else {
            category.rules = [...category.rules, JSON.parse(JSON.stringify(defaultRule(newId)))];
        }
    }

    function deleteRule(idx) {
        category.rules.splice(idx, 1)
        category.rules = [...category.rules]

        playSound(deleteCategorySound);

        // deleteCategorySound.volume = 0.3
        // deleteCategorySound.pause();
        // deleteCategorySound.currentTime = 0;
        // deleteCategorySound.play();
    }

    export let removingHoverTime = 25; // how long until we unshow hovered buttons
    let removingHover;
    function setHovering(boolean) {
        if (boolean == true) {
            if (removingHover) { clearTimeout(removingHover); }
            hovering = true
        } else {
            if (removingHover) { clearTimeout(removingHover); }
            removingHover = setTimeout(() => {
                hovering = false;
            }, removingHoverTime);
        }
    }

</script>

<div
    class="flex flex-col"
    on:mouseover={() => setHovering(true)}
    on:focus={() => setHovering(true)}
    on:mouseout={() => setHovering(false)}
    on:blur={() => setHovering(false)}
>
<div class="relative flex mb-4 border-b border-gray-300 dark:border-gray-800 focus-within:border-secondary-600">
    {#if hovering }
    <div class="absolute">
        <slot name="deleteAndChangePosBtns" />
    </div>
    {/if}
    <input
        type="text"
        class="block w-full border-0 border-b border-transparent bg-inherit focus:border-secondary-600 focus:ring-0 dark:text-secondary-300 text-secondary-700"
        placeholder="Work"
        bind:value={category.name}>
    <button class="relative dark:text-secondary-300 hover:dark:text-secondary-400 text-secondary-700 cursor-pointer"
        on:click={() => {
            category.collapsed = !category.collapsed;
        }}>
        <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6 transform {!category.collapsed ? '' : 'rotate-180'}
                    transition duration-300"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
    </button>
</div>

{#if !category.collapsed}
<ul
    transition:slide|local={{duration:600}}
    class="border-l dark:border-gray-800 border-gray-200 mt-2 mb-4 ml-2 pl-4">
    {#each category.rules as definition, i (definition.id)}
        <li out:fly|local={{x:30, duration:100}} class="mb-2">
            <SelectInputCombo options={definition.options} bind:value={category.rules[i].value} bind:selectValue={category.rules[i].selectedOption}>
                <span class="ml-4 text-sm font-extrabold text-red-400 hover:text-red-500 cursor-pointer" on:click={() => deleteRule(i)}>X</span>
            </SelectInputCombo>
        </li>
    {/each}
    <li on:click={addRule}
        class="ml-6 mt-4 text-sm dark:text-green-300 hover:dark:text-green-400 hover:text-green-500 text-green-600 cursor-pointer w-fit">
        Add Rule +
    </li>
</ul>
{/if}
</div>

<audio
    bind:this={deleteCategorySound}
    src="/static/sounds/paper_slide.wav"
></audio>