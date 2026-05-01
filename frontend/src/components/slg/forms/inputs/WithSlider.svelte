<script>
    import Slider from "../sliders/Slider2.svelte";

    export let id = "input-with-slider";

    export let label = "Temperature";
    export let labelClasses = "text-gray-800 dark:text-gray-100 text-sm";
    export let inputClasses =
        "w-16 px-3 py-1 text-gray-800 dark:text-gray-100 text-sm bg-inherit border border-gray-300 dark:border-gray-700  focus:ring-primary-500 focus:border-primary-500";

    export let min = 0;
    export let max = 2;
    export let step = 0.01;

    export let value = (max - min) / 2;

    export let disabled = false;
    export let placeholder = "";

    const clampValue = (value) => {
        return value > max ? (value = max) : value < min ? (value = min) : (value = value)
    }

    $: value = clampValue(value);
</script>

<div class="flex flex-col w-[80%]">
    <div class="flex justify-between items-center">
        <label for={id} class={labelClasses}>{@html label}</label>
        <input {id} {disabled} bind:value type="text" class={inputClasses} {placeholder} />
    </div>

    <div class="w-full">
        <Slider {min} {max} {step} bind:value />
    </div>
</div>
