<script>
    import { createEventDispatcher } from 'svelte';
    export let sections = [];
    export let selectedId = null;

    const dispatch = createEventDispatcher();

    let adding = false;
    let newName = '';
    let dragSrcId = null;
    let dragOverId = null;

    function submitAdd() {
        if (!newName.trim()) return;
        dispatch('add', { name: newName.trim(), day_configs: {} });
        newName = '';
        adding = false;
    }

    function onDragStart(e, id) {
        dragSrcId = id;
        e.dataTransfer.effectAllowed = 'move';
    }

    function onDragOver(e, id) {
        e.preventDefault();
        dragOverId = id;
    }

    function onDrop(e, targetId) {
        e.preventDefault();
        if (!dragSrcId || dragSrcId === targetId) { dragSrcId = null; dragOverId = null; return; }
        const ids = sections.map(s => s.id);
        const from = ids.indexOf(dragSrcId);
        const to = ids.indexOf(targetId);
        ids.splice(from, 1);
        ids.splice(to, 0, dragSrcId);
        dispatch('reorder', ids);
        dragSrcId = null;
        dragOverId = null;
    }

    function onDragEnd() {
        dragSrcId = null;
        dragOverId = null;
    }
</script>

<aside class="flex flex-col gap-1 min-w-0">
    <button
        on:click={() => dispatch('select', null)}
        class="w-full text-left px-3 py-2 rounded text-sm transition-colors
            {selectedId === null
                ? 'bg-indigo-600/30 text-indigo-300 font-medium'
                : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'}">
        All Tasks
    </button>

    {#each sections as s (s.id)}
        <div
            draggable="true"
            on:dragstart={(e) => onDragStart(e, s.id)}
            on:dragover={(e) => onDragOver(e, s.id)}
            on:drop={(e) => onDrop(e, s.id)}
            on:dragend={onDragEnd}
            class="group flex items-center gap-1 rounded transition-colors
                {dragOverId === s.id && dragSrcId !== s.id ? 'border-t-2 border-indigo-500' : ''}
                {dragSrcId === s.id ? 'opacity-40' : ''}
                {selectedId === s.id ? 'bg-indigo-600/30' : 'hover:bg-slate-800'}">
            <span class="pl-1 text-slate-600 group-hover:text-slate-500 cursor-grab active:cursor-grabbing shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="currentColor">
                    <circle cx="9" cy="6" r="1.5"/><circle cx="15" cy="6" r="1.5"/>
                    <circle cx="9" cy="12" r="1.5"/><circle cx="15" cy="12" r="1.5"/>
                    <circle cx="9" cy="18" r="1.5"/><circle cx="15" cy="18" r="1.5"/>
                </svg>
            </span>
            <button
                on:click={() => dispatch('select', s.id)}
                class="flex-1 min-w-0 text-left px-2 py-2 text-sm truncate transition-colors
                    {selectedId === s.id ? 'text-indigo-300 font-medium' : 'text-slate-400'}">
                {s.name}
            </button>
            <div class="flex shrink-0 opacity-0 group-hover:opacity-100 transition-opacity pr-1">
                <button on:click={() => dispatch('editRequest', s)} class="p-1 text-slate-500 hover:text-slate-200">
                    <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                    </svg>
                </button>
                <button on:click={() => dispatch('delete', s)} class="p-1 text-slate-500 hover:text-red-400">
                    <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/>
                        <path d="M10 11v6"/><path d="M14 11v6"/>
                    </svg>
                </button>
            </div>
        </div>
    {/each}

    {#if adding}
        <div class="flex gap-1.5 px-2 pt-1 pb-2">
            <input
                bind:value={newName}
                placeholder="Section name"
                on:keydown={(e) => { if (e.key === 'Enter') submitAdd(); if (e.key === 'Escape') adding = false; }}
                class="flex-1 bg-slate-800 border border-slate-600 rounded px-2 py-1.5 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
                autofocus />
            <button on:click={submitAdd} class="px-2 py-1 bg-indigo-600 hover:bg-indigo-500 text-white text-xs rounded transition-colors">Add</button>
            <button on:click={() => adding = false} class="px-2 py-1 bg-slate-700 hover:bg-slate-600 text-slate-300 text-xs rounded transition-colors">✕</button>
        </div>
    {:else}
        <button
            on:click={() => adding = true}
            class="flex items-center gap-1.5 px-3 py-1.5 text-xs text-slate-500 hover:text-slate-300 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="size-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
            Add Section
        </button>
    {/if}
</aside>
