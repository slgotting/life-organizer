
<script>
    import { onMount } from "svelte";

    export let min = 1;
    export let max = 100;
    export let value = 50;

    export let darkColorWeight = 400;
    export let colorWeight = 600;



    let color;
    let darkColor;
    function setSliderColor(darkMode) {
        color = getComputedStyle(document.querySelector(`.text-primary-${colorWeight}`)).color;
        darkColor = getComputedStyle(document.querySelector(`.text-primary-${darkColorWeight}`)).color;
    }

    onMount(async () => {
        setSliderColor();
    });

</script>




<input class="slider" type="range" min={min} max={max} value={value} style="--sliderColor: {color}; --darkSliderColor: {darkColor}" />




<style>
/* Theinput itself */
.slider {
  -webkit-appearance: none;  /* Override default CSS styles */
  appearance: none;
  width: 100%; /* Full-width */
  height: 25px; /* Specified height */
  outline: none; /* Remove outline */
  opacity: 0.7; /* Set transparency (for mouse-over effects on hover) */
  -webkit-transition: .2s; /* 0.2 seconds transition on hover */
  transition: opacity .2s;
}

/* Mouse-over effects */
.slider:hover {
  opacity: 1; /* Fully shown on mouse-over */
}

/* Theinput handle (use -webkit- (Chrome, Opera, Safari, Edge) and -moz- (Firefox) to override default look) */
.slider::-webkit-slider-thumb {
  -webkit-appearance: none; /* Override default look */
  appearance: none;
  width: 25px; /* Set a specificinput handle width */
  height: 25px; /*input handle height */
  background: var(--sliderColor); /* Green background */
  cursor: pointer; /* Cursor on hover */
}

.slider::-moz-range-thumb {
  width: 25px; /* Set a specificinput handle width */
  height: 25px; /*input handle height */
  background: var(--sliderColor); /* Green background */
  cursor: pointer; /* Cursor on hover */
}

:global(.dark .slider) {
  -webkit-appearance: none;  /* Override default CSS styles */
  appearance: none;

  width: 100%; /* Full-width */
  height: 12px; /* Specified height */
  outline: none; /* Remove outline */
  opacity: 1; /* Set transparency (for mouse-over effects on hover) */
  -webkit-transition: .2s; /* 0.2 seconds transition on hover */
  transition: opacity .2s;
  border-radius:6px;
}

/* Mouse-over effects */
:global(.dark .slider:hover) {
  opacity: 1; /* Fully shown on mouse-over */
}

/* Theinput handle (use -webkit- (Chrome, Opera, Safari, Edge) and -moz- (Firefox) to override default look) */
:global(.dark .slider::-webkit-slider-thumb) {
  -webkit-appearance: none; /* Override default look */
  appearance: none;
  width: 25px; /* Set a specificinput handle width */
  height: 25px; /*input handle height */
  background: var(--darkSliderColor); /* Green background */
  cursor: pointer; /* Cursor on hover */
  border-radius:6px;
}

:global(.dark .slider::-moz-range-thumb) {
  width: 25px; /* Set a specificinput handle width */
  height: 25px; /*input handle height */
  background: var(--darkSliderColor); /* Green background */
  cursor: pointer; /* Cursor on hover */
}
</style>