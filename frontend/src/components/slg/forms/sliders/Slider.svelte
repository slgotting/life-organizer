
<script>
    import { onMount } from "svelte";

    export let min = 1;
    export let max = 100;
    export let value = 50;

    onMount(async () => {
    });

</script>




<input class="slider" type="range" min={min} max={max} value={value} style="--sliderColor: grey; --darkSliderColor: grey" />




<style>
/* Theinput itself */
.slider {
  -webkit-appearance: none;  /* Override default CSS styles */
  appearance: none;
  background: rgb(51, 51, 51);
  width: 100%; /* Full-width */
  height: 6px; /* Specified height */
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
  width: 10px; /* Set a specificinput handle width */
  height: 10px; /*input handle height */
  background: white; /* Green background */
  cursor: pointer; /* Cursor on hover */
}

.slider::-moz-range-thumb {
  width: 10px; /* Set a specificinput handle width */
  height: 10px; /*input handle height */
  background: white; /* Green background */
  cursor: pointer; /* Cursor on hover */
}

:global(.dark .slider) {
  -webkit-appearance: none;  /* Override default CSS styles */
  appearance: none;

  width: 100%; /* Full-width */
  height: 8px; /* Specified height */
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
  width: 10px; /* Set a specificinput handle width */
  height: 10px; /*input handle height */
  background: white; /* Green background */
  cursor: pointer; /* Cursor on hover */
  border-radius:6px;
}

:global(.dark .slider::-moz-range-thumb) {
  width: 10px; /* Set a specificinput handle width */
  height: 10px; /*input handle height */
  background: white; /* Green background */
  cursor: pointer; /* Cursor on hover */
}
</style>