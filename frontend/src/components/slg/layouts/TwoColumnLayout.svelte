<script>
    // see no purge section for all tailwind supported options. add options as needed
    export let breakpoint = "lg";

</script>

<!-- No purge section -->
<!--
sm:flex-row
md:flex-row
lg:flex-row
xl:flex-row
sm:w-96
md:w-96
lg:w-96
xl:w-96
-->

<div
    class="flex flex-col {breakpoint}:flex-row">
    <div class="flex-1">
        <div class="py-6 px-4 sm:px-6 lg:px-8">
            <slot name="left" />
        </div>
    </div>

    <div class="{breakpoint}:w-96">
        <div class="inset-0 py-6 px-4 sm:px-6 lg:px-8">
            <slot name="right" />
        </div>
    </div>
</div>
