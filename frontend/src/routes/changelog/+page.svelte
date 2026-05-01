
<script>

    import Change from "./Change.svelte";

</script>


<div class="flex flex-col items-center text-daw-gray-800">

    <div class="flex flex-col justify-center items-center">
        <div class="text-4xl font-extrabold">Changelog</div>
        <div class="text-[0.7rem] font-extralight">*Only the stuff you might find interesting</div>
    </div>

    <div class="mt-4 space-y-2">
        <Change version={"v1.0.0"} date={""}
            changes={[ "Initial Release" ]}
        />
    </div>

</div>
