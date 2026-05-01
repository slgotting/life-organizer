
<div class="relative">
    <div id="text" class="text-sm text-center perfect-center">
        Applying Flux
    </div>
    <!-- <Loader /> -->
    <div class="container">
    <div class="liquid"></div>
    <div class="liquid"></div>
    <div class="liquid"></div>
    <div class="liquid"></div>
    </div>
    <svg>
    <filter id="gooey">
        <feGaussianBlur in="SourceGraphic" stdDeviation="10" />
        <feColorMatrix values="
            1 0 0 0 0
            0 1 0 0 0
            0 0 1 0 0
            0 0 0 20 -10
            " />
    </filter>
    </svg>
</div>


<style>

:root {
  --containerSize: 150px;
  --liquidSize: 40px;
  --ani_dur: 2s;
}

.container {
  position: relative;
  /* width: 250px;
  height: 250px; */
  width: var(--containerSize);
  height: var(--containerSize);
  margin: 4rem;
  animation: rotate var(--ani_dur) ease-out infinite;
  filter: url("#gooey");
}
@keyframes rotate {
  0% {
    transform: rotate(360deg);
  }
  50% {
    transform: rotate(360deg);
  }
  100% {
    transform: rotate(0deg);
  }
}
.container .liquid {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: linear-gradient(45deg, #c7eeff, #03a9f4);
  width: var(--liquidSize);
  height: var(--liquidSize);
  border-radius: 50%;
}
#text {
    animation: animateVis var(--ani_dur) ease-out infinite;
}
.container .liquid:nth-child(1) {
  top: 0;
  animation: animate1 var(--ani_dur) linear infinite;
}
.container .liquid:nth-child(2) {
  left: 0;
  animation: animate2 var(--ani_dur) linear infinite;
}
.container .liquid:nth-child(3) {
  left: 100%;
  animation: animate3 var(--ani_dur) linear infinite;
}
.container .liquid:nth-child(4) {
  top: 100%;
  animation: animate4 var(--ani_dur) linear infinite;
}
@keyframes animateVis {
  0% {
    opacity: 1;
  }
  20% {
    opacity: 0;
  }
  50% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
@keyframes animate1 {
  0% {
    top: 0;
  }
  50% {
    top: 100%;
  }
  100% {
    top: 100%;
  }
}
@keyframes animate2 {
  0% {
    left: 0;
  }
  50% {
    left: 100%;
  }
  100% {
    left: 100%;
  }
}
@keyframes animate3 {
  0% {
    left: 100%;
  }
  50% {
    left: 0;
  }
  100% {
    left: 0;
  }
}
@keyframes animate4 {
  0% {
    top: 100%;
  }
  50% {
    top: 0;
  }
  100% {
    top: 0;
  }
}
svg {
  width: 0;
  height: 0;
}
    .perfect-center {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }

</style>