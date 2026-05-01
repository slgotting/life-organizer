<script>
//   import Time from "slgotting-times";

  export let format = "";
  export let range = [];
  //   export let start = "9 AM";
  //   export let end = "12 PM";
  export let color = "green-400";
</script>

<style>

</style>

<!-- <div
  class="flex border px-2 text-sm rounded-md bg-green-400 border-green-400
  shadow-md text-white"
  style="width: fit-content; width: -moz-fit-content;"> -->
<div
  class="px-2 text-sm rounded-md bg-{color} shadow-md text-white
  whitespace-no-wrap">
  {range[0]} - {range[1]}
</div>
<!-- </div> -->
