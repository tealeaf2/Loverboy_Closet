<script setup>

</script>

<template>
  <div class="container">
    <li style="--t:20%">
      <a href="#">
        <strong>
          Top
        </strong>
      </a>
    </li>
    <li style="--t:30%">
      <a href="#">
        <strong>
          Sweaters
        </strong>
      </a>
    </li>
    <li style="--t:40%">
      <a href="#">
        <strong>
          Suit
        </strong>
      </a>
    </li>
    <li style="--t:50%">
      <a href="#">
        <strong>
          Innerwear
        </strong>
      </a>
    </li>
    <li style="--t:60%">
      <a href="#">
        <strong>
          Accessories
        </strong>
      </a>
    </li>
    <div class="top"></div>
    <div class="middle"></div>
    <div class="bottom"></div>
  </div>
</template>

<style scoped>
  *{
    margin: 0;
    padding: 0;
  }
  .container{
    width: 15px;
    height: 600px;
    position: fixed;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    border-radius: 0 15px 15px 0;
    overflow: hidden;
    transition: 0.3s;
    background-color: var(--third-color);
    z-index: 3;
  }
  .container:hover{
    width: 150px;
    border-radius: 0 30px 30px 0;
  }
  .container:hover li a{
    color: #fff;

  }
  .container:hover .middle{
    height: 10%;
  }
  /* .container::before{
    content: "";
    width: 50%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    z-index: -1;
    background-color: lightseagreen;
  } */
  .container .top{
    width: 100%;
    height: 20%;
    background-color: var(--third-color);
    transition: 0.2s;
  }
  .container .middle{
    width: 100%;
    height: 0%;
    background-color: var(--primary-color);


  }
  .container .bottom{
    width: 100%;
    height: 100%;
    background-color: var(--third-color);
  }
  .container li{
    position: absolute;
    top: var(--t);
    width: 100%;
    height: 10%;
    font-size: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .container li a{
    color: transparent;
    transition: 0.3s;
    text-decoration: none;
  }
  .container li:nth-child(1):hover ~.top{
    height: 20%;
  }
  .container li:nth-child(2):hover ~.top{
    height: 30%;
  }
  .container li:nth-child(3):hover ~.top{
    height: 40%;
  }
  .container li:nth-child(4):hover ~.top{
    height: 50%;
  }
  .container li:nth-child(5):hover ~.top{
    height: 60%;
  }

</style>