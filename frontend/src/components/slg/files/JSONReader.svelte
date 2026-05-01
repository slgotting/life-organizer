<script>
    export let example = false;

    import Dropzone from "svelte-file-dropzone";

    export let jsonData;

    let files = [];
    let fileUploaded = false;

    function handleFilesSelect(e) {
        files = e.detail.acceptedFiles;
        for (let i = 0; i < files.length; i++) {
            const reader = new FileReader();
            reader.onload = () => {
                const binaryStr = reader.result;
                jsonData = processRawJson(binaryStr);
                fileUploaded = true;
            };
            reader.readAsText(files[i]);
        }
    }

    function processRawJson(data) {
        return JSON.parse(data);
    }

    function resetAll() {
        fileUploaded = false;
        files = [];
        jsonData = null;
    }
</script>

{#if example}
    <svelte:self bind:jsonData>Example Drop JSON here</svelte:self>
{:else}
    {#if fileUploaded}
        <Dropzone containerClasses="dark:!bg-gray-800 dark:!border-gray-700 dark:!text-gray-400 !text-gray-600 !bg-gray-200 !border-gray-400" disabled="true">
            <div class="flex">
                <p class="">{files[0].name}</p>
                <button on:click={() => resetAll()}
                        class="ml-4">
                    <svg class="w-6 h-6 text-red-400 hover:text-red-500 cursor-pointer" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 22 22">
                        <path
                            style="fill:currentColor;fill-opacity:1;stroke:none"
                            d="M 8 3 L 0.94335938 10.056641 L 0 11 L 0.94335938 11.943359 L 8 19 L 20.333984 19 L 22 19 L 22 3 L
                        20.333984 3 L 8 3 z M 11.320312 7 L 14 9.6796875 L 16.679688 7 L 18 8.3203125 L 15.320312 11 L 18 13.679688
                        L 16.679688 15 L 14 12.320312 L 11.320312 15 L 10 13.679688 L 12.679688 11 L 10 8.3203125 L 11.320312 7 z "
                            class="ColorScheme-Text" />
                    </svg>
                </button>
            </div>
        </Dropzone>
    {:else}
        <Dropzone containerClasses="dark:!bg-gray-800 dark:!border-gray-700 cursor-pointer dark:!text-gray-400 !text-gray-600 !bg-gray-200 !border-gray-400"
                  on:drop={handleFilesSelect} accept={[".json"]}>
            <slot />
        </Dropzone>
    {/if}
{/if}
