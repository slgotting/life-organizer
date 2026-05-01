<script>
    import { onMount, onDestroy } from "svelte";
    import { Chart } from "frappe-charts";

    /**
     *  PROPS
     */
    export let data = {
        labels: [],
        datasets: [{ values: [] }],
        yMarkers: {},
        yRegions: [],
    };
    export let title = "";
    export let type = "line";
    export let height = 300;
    export let animate = true;
    export let axisOptions = {};
    export let barOptions = {};
    export let lineOptions = {};
    export let tooltipOptions = {};
    export let colors = [];
    export let valuesOverPoints = 0;
    export let isNavigable = false;
    export let maxSlices = 3;

    let chartRef;
    let chartDrawn;
    let chartGlobal; // the reason for chartGlobal is that if I create the reference directly with chart, it fails to create new graphs

    onMount(() => {
        drawChart(data);
    })

    $: updateData(data);

    export function exportChart() {
        if (chartGlobal) {
            chartGlobal.export();
        }
    }

    function updateData(data) {
        if (chartDrawn) {
            drawChart(data);
        }
    }

    function drawChart(data) {
        const chart = new Chart(chartRef, {
            data,
            title,
            type,
            height,
            animate,
            colors,
            axisOptions,
            barOptions,
            lineOptions,
            tooltipOptions,
            valuesOverPoints,
            isNavigable,
            maxSlices,
        });
        chartDrawn = true
        chartGlobal = chart;
    }

</script>


<div bind:this={chartRef} on:data-select />