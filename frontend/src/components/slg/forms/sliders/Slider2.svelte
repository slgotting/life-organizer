<!-- @format -->
<script>
    import { onMount } from "svelte";

    export let min = 0;
    export let max = 2;
    export let step = 0.01;

    export let value = (max - min) / 2;

    const sliderProps = {
        fill: "white",
        background: "rgba(255, 255, 255, 0.214)",
    };

    let slider;

    onMount(() => {
        // Using Event Listener to apply the fill and also change the value of the text.
        slider.addEventListener("input", (event) => {
            applyFill(event.target);
        });
        applyFill(slider);
        function applyFill(slider) {
            const percentage = (100 * (slider.value - slider.min)) / (slider.max - slider.min);
            const bg = `linear-gradient(90deg, ${sliderProps.fill} ${percentage}%, ${sliderProps.background} ${percentage + 0.1}%)`;
            slider.style.background = bg;
        }
    });
</script>
<input bind:this={slider} id="slider" type="range" {min} {max} {step} bind:value />
<style>
    #slider {
        -webkit-appearance: none;
        width: 100%;
        height: 2px;
        border-radius: 5px;
        background: rgba(255, 255, 255, 0.314);
        outline: none;
        padding: 0;
        margin: 0;
        cursor: pointer;
    }
    #slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: white;
        cursor: pointer;
        transition: all 0.15s ease-in-out;
    }
    #slider::-webkit-slider-thumb:hover {
        background: #d4d4d4;
        transform: scale(1.2);
    }
    #slider::-moz-range-thumb {
        width: 10px;
        height: 10px;
        border: 0;
        border-radius: 50%;
        background: white;
        cursor: pointer;
        transition: background 0.15s ease-in-out;
    }
    #slider::-moz-range-thumb:hover {
        background: #d4d4d4;
    }
</style>
