

<div class="box"></div>


<style>


.box {
  position: relative;
  background: rgb(80, 80, 231);
  border: 0.25rem solid #363636;
  box-sizing: border-box;
  height: 4rem;
  width: 4rem;
  outline: 0;
  overflow: hidden;
}
.box::before {
  content: "Applying Flux";
  font-family: Arial;
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.box::after {
  content: "";
  position: absolute;
  bottom: -50%;
  left: -50%;
  height: 200%;
  width: 200%;
  box-sizing: border-box;
  background-color: #fff;
  border-radius: 40%;
  animation: spin 6s linear infinite;
}

@keyframes spin {
  0% {
    transform: translateY(0) rotate(0deg);
  }
  100% {
    transform: translateY(-100%) rotate(360deg);
  }
}
</style>