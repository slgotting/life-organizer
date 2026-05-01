<script>
    import IconList from "../lists/IconList.svelte";
    import BaseModal from "../modals/BaseModal.svelte";
    import Button from "../primitives/Button.svelte";
    import LinkNewTab from '../links/LinkNewTab.svelte';

    export let example = false

    export let projectName = 'App'
    export let description = 'Some information about the app'
    export let side = "left"
    export let link = "timetrack.slgotting.com"
    export let notAvailableYet = false;

    export let bgColor = "bg-slate-800 dark:bg-white";
    export let ringColor = "dark:ring-gray-900 ring-white"
    export let ringSize = "ring-4"
    export let frontendTech = [
        'Svelte',
        'TailwindCSS',
        'Javascript'
    ]
    export let backendTech = [
        'Python',
        'Flask',
        'MongoDB',
        'nginx',
    ]
    export let devopsTech = [
        'Digital Ocean',
        'Github Actions',
        'Docker',
    ]

    let moreInfoModal;
</script>


{#if example}

    <svelte:self />

{:else}


<div class="px-4 xl:px-0">

<h3 class="text-lg font-medium text-gray-900 dark:text-gray-50">
    {projectName}
</h3>
<p class="mt-2 text-sm text-gray-500">
    {description}
</p>

    {#if frontendTech.length > 0}
    <div class="flex flex-col mt-4">
        <h2 class="text-sm">Frontend</h2>
        <IconList height="h-10"
            icons={frontendTech}
            {bgColor}
            {ringColor}
            {ringSize}
        />
    </div>
    {/if}
    {#if backendTech.length > 0}
    <div class="flex flex-col mt-2">
        <h2 class="text-sm">Backend</h2>
        <IconList height="h-10"
            icons={backendTech}
            {bgColor}
            {ringColor}
            {ringSize}
        />
    </div>
    {/if}
    {#if devopsTech.length > 0}
    <div class="flex flex-col mt-2">
        <h2 class="text-sm">DevOps</h2>
        <IconList height="h-10"
            icons={devopsTech}
            {bgColor}
            {ringColor}
            {ringSize}
        />
    </div>
    {/if}

    {#if side == "right"}

    <div class="flex justify-start items-center mt-4">
        {#if notAvailableYet}
            <div class="text-sm text-secondary-600 dark:text-secondary-400 transition ease-in-out duration-150">
                In the process of publishing...
            </div>
        {:else}
        <div class="flex justify-center items-center">
            <div class="text-secondary-600 hover:text-secondary-500 dark:text-secondary-400 hover:dark:text-secondary-500">
                <LinkNewTab href="{ link }" text="Visit" direction="left" />
            </div>
            <!-- <a href="{ link }" class="text-secondary-600 hover:text-secondary-500 dark:text-secondary-400 hover:dark:text-secondary-500 transition ease-in-out duration-150">
                <span aria-hidden="true">&larr;</span> Visit</a> -->
        </div>
        {/if}
        <div class="ml-6">
            <Button on:click={() => moreInfoModal.openModal()}>More info</Button>
        </div>
        <BaseModal bind:this={moreInfoModal} position={"middle-center"} >
            <slot name="moreInfoModal">
            </slot>
        </BaseModal>
    </div>

    {:else if side == "left"}

    <div class="flex justify-end items-center mt-4">
        <div class="mr-6">
            <Button
                on:click={() => moreInfoModal.openModal()}
                colors="bg-primary-600 hover:bg-primary-700 focus:ring-primary-500"
            >
                More info
            </Button>
        </div>
        {#if notAvailableYet}
        <div class="flex justify-center items-center">
            <div class="text-sm text-secondary-600 dark:text-secondary-400 transition ease-in-out duration-150">
                In the process of publishing...
            </div>
            <!-- <button on:click={showNotReady} class="text-secondary-600 hover:text-secondary-500 dark:text-secondary-400 hover:dark:text-secondary-500 transition ease-in-out duration-150">Visit <span aria-hidden="true">&rarr;</span></button> -->
        </div>
        {:else}
        <div class="flex justify-center items-center">
            <div class="text-secondary-600 hover:text-secondary-500 dark:text-secondary-400 hover:dark:text-secondary-500">
                <LinkNewTab href="{ link }" text="Visit" direction="right" />
            </div>
        </div>
        {/if}
        <BaseModal bind:this={moreInfoModal} position={"middle-center"} >
            <slot name="moreInfoModal">
            </slot>
        </BaseModal>
    </div>

    {/if}

</div>

{/if}