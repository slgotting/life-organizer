<script>
    import BaseModal from "../modals/BaseModal.svelte";

    export let example = false;

    export let open = false;
    export let canOpen = true;
    export let position = 'middle-center'

    export let deleteCallback = () => {alert('Nothing has been assigned to be deleted')};

    function openModal() {
        if (canOpen) {
            open = true;
        }
    }
    function close() {
        open = false;
    }
</script>

{#if example}

    <button on:click={openModal}>Open Modal</button>
    <svelte:self bind:open={open} bind:canOpen={canOpen} position={position}>
        <div slot="title">Delete Category</div>
        <div slot="description">Are you sure you want to delete this category?</div>
    </svelte:self>

{:else}

    <BaseModal
        bind:open={open}
        bind:canOpen={canOpen}
        position={position}
    >
        <!-- <div class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
            <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" />

                <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span> -->

                <div
                     class="inline-block align-bottom rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:align-middle sm:max-w-lg sm:w-full">
                    <div class="dark:bg-slate-600 bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                        <div class="sm:flex sm:items-start">
                            <div
                                 class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-50 sm:mx-0 sm:h-10 sm:w-10">
                                <!-- Heroicon name: outline/exclamation -->
                                <svg class="h-6 w-6 text-red-600" xmlns="http://www.w3.org/2000/svg" fill="none"
                                     viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            stroke-width="2"
                                            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                    </svg>
                            </div>
                            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                                <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white" id="modal-title">
                                    <slot name="title">
                                        Delete
                                    </slot>
                                </h3>
                                <div class="mt-2">
                                    <p class="text-sm text-gray-500 dark:text-gray-300">
                                        <slot name="description">
                                            Are you sure you want to?
                                        </slot>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="bg-gray-50 dark:bg-slate-600 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                        <button type="button"
                                on:click={() => {
                                    close();
                                    deleteCallback();
                                }}
                                class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm">

                            <slot name="deleteText">
                                Delete
                            </slot>
                        </button>
                        <button type="button"
                                on:click={close}
                                class="mt-3 w-full inline-flex justify-center rounded-md border-gray-300 px-4 py-2  text-sm font-medium text-gray-400 hover:text-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-secondary-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                            <slot name="cancelText">
                                Cancel
                            </slot>
                        </button>
                    </div>
                </div>
            <!-- </div>
        </div> -->

    </BaseModal>
{/if}
