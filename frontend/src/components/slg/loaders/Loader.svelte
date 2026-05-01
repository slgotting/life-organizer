
<script>
    export let size = "size-6"
</script>

<!-- This fantastic loader was provided by Eli Moyal at https://codepen.io/emoyal4 -->
<svg class="{size}" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="50" cy="50" r="45" />
</svg>

<style>

svg {
  animation: rotate 2s linear infinite reverse;
}
svg circle {
  stroke: #bdbec3;
  stroke-width: 7;
  stroke-dasharray: 283px;
  stroke-dashoffset: -283px;
  animation: load 2.8s cubic-bezier(0.53, 0.11, 0.57, 0.91) infinite;
}
@keyframes load {
  from {
    stroke-dashoffset: -283px;
  }
  to {
    stroke-dashoffset: 283px;
  }
}
@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

</style>