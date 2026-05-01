<script>
    import { onMount } from "svelte";

    export let animStartTime = 0;

    let main;

    function updateStartTime(startTime) {
        for (const elem of Array.from(main.querySelectorAll('span'))) {
            elem.style.animationDelay = startTime;
        }
        // going with span only for now to really get weird
        // for (const elem of Array.from(document.querySelectorAll('div'))) {
        //     elem.style.animationDelay = startTime;
        // }
    }

    onMount(() => {
        updateStartTime(animStartTime);
    });

</script>

<!-- This amazing loader was provided by Eli Moyal at https://codepen.io/emoyal4/pen/qBXRYGV -->
<main bind:this={main}>
  <div>
    <div>
      <span></span>
    </div>
    <div>
      <span></span>
    </div>
  </div>

  <span>
    <span></span>
   </span>

  <span>
    <span></span>
   </span>

  <span>
    <span></span>
   </span>

    <span>
    <span></span>
   </span>

    <span>
    <span></span>
   </span>

</main>

<style>

    main {
        position: relative;
        /* background: #000; */
        overflow: hidden;
        background: #00235324;
        height: 100%;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        filter: blur(8px) contrast(18);
        mix-blend-mode: screen;
    }
    main > span {
        position: absolute;
    }
    main > span:nth-of-type(1) {
        left: 50%;
        width: 150px;
        height: 150px;
        animation: spin-3 8s ease-in-out infinite forwards;
    }
    main > span:nth-of-type(1) span {
        width: 30px;
    }
    main > span:nth-of-type(2) {
        left: 20%;
        width: 150px;
        height: 100px;
        animation: spin-4 6s ease-in-out infinite;
    }
    main > span:nth-of-type(2) span {
        width: 21px;
    }
    main > span:nth-of-type(3) {
        left: 48%;
        top: 48%;
        width: 100px;
        height: 100px;
        animation: spin-5 3.5s ease-in-out infinite forwards;
    }
    main > span:nth-of-type(3) span {
        width: 25px;
    }
    main > span:nth-of-type(4) {
        left: 28%;
        top: 48%;
        width: 200px;
        height: 200px;
        animation: spin-2 4.5s ease-in-out infinite forwards;
    }
    main > span:nth-of-type(4) span {
        width: 20px;
    }
    main > span:nth-of-type(5) {
        left: 50%;
        top: 25%;
        width: 165px;
        height: 165px;
        animation: spin-6 3.5s ease-in-out infinite forwards;
    }
    main > span:nth-of-type(5) span {
        width: 20px;
    }
    main > span > span {
        position: absolute;
        /* background: #0271ff; */
        background: #fff;
        right: 20px;
        top: 20px;
        aspect-ratio: 1;
        border-radius: 50%;
    }

    div {
        position: relative;
        width: 80px;
        aspect-ratio: 1;
        /* background: #60a5fa; */
        background: #fff;
        border-radius: 50%;
    }
    div > div {
        position: absolute;
        aspect-ratio: 1;
        border-radius: 50%;
        background: transparent;
    }
    div > div > span {
        position: absolute;
        aspect-ratio: 1;
        /* background: #60a5fa; */
        background: #fff;
        border-radius: 50%;
    }
    div > div:nth-child(1) {
        left: -5px;
        width: 70px;
        animation: spin-1 5s ease-in infinite forwards;
    }
    div > div:nth-child(1) > span {
        width: 50px;
    }
    div > div:nth-child(2) {
        left: 10px;
        bottom: 0;
        width: 80px;
        animation: spin-2 3s ease-in 1.5s infinite forwards;
    }
    div > div:nth-child(2) > span {
        width: 60px;
    }

    @keyframes spin-1 {
        0% {
            transform: rotate(90deg);
        }
        100% {
            transform: rotate(450deg);
        }
    }
    @keyframes spin-2 {
        0% {
            transform: rotate(-50deg);
        }
        100% {
            transform: rotate(310deg);
        }
    }
    @keyframes spin-3 {
        0% {
            transform: rotate(220deg);
        }
        100% {
            transform: rotate(580deg);
        }
    }
    @keyframes spin-4 {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
    @keyframes spin-5 {
        0% {
            transform: rotate(-100deg);
        }
        100% {
            transform: rotate(260deg);
        }
    }
    @keyframes spin-6 {
        0% {
            transform: rotate(210deg);
        }
        100% {
            transform: rotate(570deg);
        }
    }
</style>
