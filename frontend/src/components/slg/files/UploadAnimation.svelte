
<!-- https://codepen.io/emoyal4/details/gOGYrOm -->

<script>
function buttonClicked(){
  elBtn = document.querySelector('.btn')
  elBtn.classList.toggle('click')

}
</script>

<div class="btn" on:click={buttonClicked}>
  <span><i class="fas fa-arrow-up"></i></span>
  <h1>Upload File</h1>
    <h2><i class="fas fa-check"></i>Uploaded</h2>
</div>

<link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css" integrity="sha384-AYmEC3Yw5cVb3ZcuHtOA93w35dYTsvhLPVnYs9eStHfGJvOvKxVfELGroGkvsg+p" crossorigin="anonymous"/>

<style>

.btn {
  position: relative;
  width: 150px;
  height: 50px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 5px 5px 10px 1px #0002;
  overflow: hidden;
  cursor: pointer;
}
.btn:before {
  content: "";
  position: absolute;
  background: #2d3142;
  top: 50%;
  left: 50%;
  transform: translate(-150%, -50%);
  width: 135%;
  height: 400%;
  border-radius: 50px;
}
.btn.click:before {
  animation: background 1s ease-in 1s forwards;
}
.btn.click h1 {
  animation: upload-text 1s linear forwards;
}
.btn.click h2 {
  animation: end-txt 2.5s linear 0.1s forwards;
}
.btn.click span {
  animation: move-icon 2.5s linear 0.3s forwards;
}
.btn h1,
.btn h2 {
  position: absolute;
  margin: 0;
  white-space: nowrap;
  font-size: 16px;
}
.btn h1 {
  top: 16.5px;
  left: 45px;
  color: #2c3d55;
}
.btn h2 {
  top: 116.5px;
  left: 27px;
  color: #efefef;
  display: flex;
  gap: 10px;
}
.btn span {
  position: absolute;
  top: 17px;
  left: 18px;
  color: #2c3d55;
}

@keyframes upload-text {
  0% {
    left: 45px;
    transform: scalex(1);
  }
  25% {
    left: 35px;
    transform: scalex(0.9);
  }
  30% {
    transform: scalex(1);
  }
  100% {
    left: 245px;
  }
}
@keyframes background {
  0% {
    transform: translate(-150%, -50%) rotate(0deg);
  }
  100% {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}
@keyframes move-icon {
  0% {
    left: 18px;
    top: 17px;
  }
  20% {
    left: 70px;
    top: 17px;
  }
  40% {
    color: #000c;
  }
  65% {
    left: 70px;
    top: 17px;
    color: #fff;
  }
  78% {
    left: 70px;
    top: 25px;
  }
  100% {
    left: 70px;
    top: -200px;
    color: #fff;
  }
}
@keyframes end-txt {
  0% {
    top: 116.5px;
  }
  70% {
    top: 116.5px;
  }
  100% {
    top: 16.5px;
  }
}


</style>