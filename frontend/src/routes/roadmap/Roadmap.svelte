

<script>
    import Item from "./Item.svelte";
</script>


<div class="my-24 flex flex-col justify-center items-center">
    <div class="flex flex-col justify-center items-center">
        <div class="text-4xl font-extrabold">Roadmap</div>
        <div class="text-xs font-extralight">In no particular order</div>
    </div>

    <div class="flex flex-col sm:flex-row mt-8 space-y-8 sm:space-y-0 sm:space-x-4">
        <Item name={"Essential"}
            items={[
                '<li class="line-through">AI Name and Tag Generation</li>',
            ]}
        />
        <Item name={"Non-Essential"}
            items={[
                '<li>"How many" feature</li>',
            ]}
        />
    </div>
</div>