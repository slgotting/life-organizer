<!-- @format -->
<script>
    import Header from "./Header.svelte";
    import TestimonialCards from "./TestimonialCards.svelte";
    import LifetimePrice from "./LifetimePrice.svelte";
    import ScrollDown from "../slg/scroll/buttons/ScrollDown.svelte";
    import PricingSection1 from "./PricingSection1.svelte";
    import PricingSection2 from "./PricingSection2.svelte";
    import FeatureList from "./FeatureList.svelte";
    import NeuronImage from "./NeuronImage.svelte";
    import Roadmap from "../../routes/roadmap/Roadmap.svelte";

    function randomPos() {
        let rotation = Math.round(Math.random() * 30, 2)
        return {
            left: Math.round(Math.random() * 100, 2),
            top: Math.round(Math.random() * 100, 2),
            rotation: Math.random() < 0.5 ? rotation : rotation * -1,
        };
    }

    function minDistanceFromOthers(position, others) {
        let min = 100;
        for (const other of others) {
            let dist = distance(position, other);
            if (dist < min) {
                min = dist
            }
        }
        return min;
    }

    function distance(a, b) {
        return Math.sqrt(Math.pow(b.left - a.left,2), Math.pow(b.top - a.top,2))
    }

    function generateRandomPositions(n = 10) {
        const output = [];
        let i = n;
        while (i > 0) {
            let pos = randomPos();
            while (minDistanceFromOthers(pos, output) < 10) {
                pos = randomPos();
            }
            output.push(pos);
            i--;
        }
        return output;
    }

    const neuronPositions = generateRandomPositions(8);

    function startDemo() {
        console.log("starting demo");
    }
</script>
<div>
    <div class="relative">
        <div class="relative z-20">
            <Header on:startDemo={startDemo} />
        </div>
        <div class="z-10">
            {#each neuronPositions as pos}
                <div class="fixed text-gray-700" style="left: {pos.left}%; top: {pos.top}%; transform: rotate({pos.rotation}deg)">
                    <NeuronImage size={"size-96"} classes={"fixed"} />
                </div>
            {/each}
        </div>
    </div>

    <!-- <div class="flex justify-center w-full relative mt-16">
        <ScrollDown name="" href="" shouldScroll={false}  />
    </div> -->
    <br />
    <br />

    <div class="relative">
        <div class="z-20 relative py-24 sm:py-36">
            <FeatureList
                headline={"Everything you need"}
                title={"Build a more flexible understanding"}
                description={'Studies show that changing the wording of a question can prevent "recognition" based understanding, fostering deeper comprehension and flexible recall. This approach enhances critical thinking, reduces cue dependency, and improves engagement by varying question formats and difficulty levels.'}
                features={[
                    {
                        name: "Enhance Critical Thinking",
                        description:
                            "Encourage deeper understanding by presenting questions in varied formats, challenging you to think critically rather than memorizing answers.",
                    },
                    {
                        name: "Improve Recall Flexibility",
                        description:
                            "Strengthen the ability to recall information in different contexts, making it easier to apply knowledge in real-world scenarios.",
                    },
                    {
                        name: "Prevent Over-Reliance on Cues",
                        description:
                            "Reduce dependency on specific cues by altering the phrasing and context of questions, leading to more robust knowledge retention.",
                    },
                    {
                        name: "Enhance Long-Term Retention",
                        description: "Improve long-term memory retention by repeatedly challenging the brain to recall information in diverse ways.",
                    },
                ]} />
        </div>

    </div>

    <!-- <TestimonialCards /> -->

    <LifetimePrice expirationDate={"|UPDATE_ME|"} price={"|UPDATE_ME|"} />

    <PricingSection2 headline={"Build a better knowledge foundation."} description={""} paymentOptions={["monthly"]} freePlanAddition={true} />

    <Roadmap />
</div>
