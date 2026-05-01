<!-- @format -->
<script>
    import Modal from "./slg/modals/BaseModal.svelte";
    import Button from "../components/slg/primitives/Button.svelte";
    import Input from "../components/slg/forms/inputs/Simple.svelte";
    import InputWithSlider from "../components/slg/forms/inputs/WithSlider.svelte";
    import Select from "../components/slg/forms/selects/Simple.svelte";
    import Info from "../components/slg/informative/Info.svelte";
    import SoundTest from "../components/slg/media/audio/SoundTest.svelte";
    import { SOUNDS } from '../lib/sounds'
    import Loader from "../components/slg/loaders/Loader.svelte";
    import { authStore } from "../stores/auth";
    import { getSettingsServer, updateSettingsServer, getSettingsLocal } from '../lib/settings'
    import { settingsModalOpenStore, settingsStore } from "../stores/settings";
    import { onMount } from "svelte";

    export let isOpen;

    let settingsLoaded = false;

    // let notifyInterval = 6;
    // let timesUpSound = "Female 1";
    let volume = 0.8;
    let animationVolume = 0.4;
    let volumeScaled = volume * 100;
    let animationVolumeScaled = animationVolume * 100;

    async function onOpen(isOpen) {
        if (isOpen) {
            if (!settingsLoaded) {
                ({volume, animationVolume} = await getSettingsLocal());
                volumeScaled = volume * 100;
                animationVolumeScaled = animationVolume * 100;
                settingsLoaded = true;
            }
        }
    }

    onMount(async () => {
        if ($authStore.isAuthenticated) {
            ({volume, animationVolume} = await getSettingsLocal());
            volumeScaled = volume * 100;
            animationVolumeScaled = animationVolume * 100;
            settingsLoaded = true;
        }
    });

    $: onOpen(isOpen);

    $: volume = volumeScaled / 100;
    $: animationVolume = animationVolumeScaled / 100;

</script>
<Modal
    bind:open={isOpen}
    onClose={() => {
        settingsModalOpenStore.set(false);
    }}
>
    <div class="relative w-96 max-h-[28rem] overflow-y-auto flex flex-col items-center p-4 bg-white dark:bg-gray-700 text-white rounded-md shadow-md text-sm">
        {#if !$authStore.isAuthenticated}
            <div class="p-16 font-bold text-lg text-center">Must be logged in to access settings</div>
        {:else}
            {#if settingsLoaded}
                <div class="flex flex-col space-y-4">
                    <!-- <div class="relative">
                        <div>Notify every:</div>
                        <div class="mb-1 pl-4 text-daw-gray-600 text-xs">How often to get notifications / reminders (0 for never)</div>
                        <div class="flex items-center">
                            <Input
                                labelClasses={"block text-sm font-medium text-gray-700 dark:text-gray-200"}
                                inputClasses={"input-number-base w-24"}
                                label={""}
                                bind:value={notifyInterval}
                                placeholder={""} />
                            <div class="ml-2">hours</div>
                        </div>
                    </div> -->
                    <!-- <div class="relative">
                        <div>Times Up Sound</div>
                        <div class="flex items-center">
                            <div class="flex-grow">
                                <Select
                                    buttonClasses={"bg-inherit relative w-full border dark:border-gray-600 border-gray-300 dark:text-gray-50 text-gray-800 rounded-md shadow-sm pl-3 pr-10 py-2 text-left cursor-default focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"}
                                    label={""}
                                    options={["Male 1", "Male 2", "Female 1", "Female 2", "Ding"]}
                                    bind:value={timesUpSound}
                                />
                            </div>
                            <div class="w-12 pl-4 flex-shrink">
                                <SoundTest
                                    soundPath={timesUpMap[timesUpSound]}
                                    vol={volume}
                                />
                            </div>
                        </div>
                    </div> -->
                    <div class="relative w-full">
                        <div class="flex items-center justify-center">
                            <InputWithSlider
                                id={"volume-slider"}
                                label="Volume"
                                min={0}
                                max={100}
                                step={1}
                                bind:value={volumeScaled}
                            />
                            <SoundTest
                                soundPath={"sounds/time-up/ding.mp3"}
                                vol={volume}
                            />
                        </div>
                    </div>
                    <div class="relative w-full">
                        <div class="flex items-center justify-center">
                            <InputWithSlider
                                id={"animation-volume-slider"}
                                label="Animation Volume"
                                min={0}
                                max={100}
                                step={1}
                                bind:value={animationVolumeScaled}
                            />
                            <SoundTest
                                soundPath={"sounds/time-up/ding.mp3"}
                                vol={animationVolume}
                            />
                        </div>
                    </div>
                </div>
                <div class="mt-8">
                    <Button
                        size="md"
                        on:click={async () => {
                            const settingsDict = await updateSettingsServer(
                                volume,
                                animationVolume
                            );
                            settingsStore.set(settingsDict);
                            isOpen = false;
                        }}>
                        Save
                    </Button>
                </div>
            {:else}
                <div class="w-80 h-80 flex items-center justify-center">
                    <div class="w-12 h-12">
                        <Loader />
                    </div>
                </div>
            {/if}
        {/if}
    </div>
</Modal>
