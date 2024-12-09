<script setup>
import { ref } from 'vue';
const scrollTarget = ref(null)
function schrollDown(){
  scrollTarget.value.scrollIntoView({ behavior: "smooth" , block: 'end'});
}
</script>
  
<template>
  <Header></Header>
  <div class="hero-box">
    <h1 class="hero up">
      <span><a>Dress </a></span>
      <span><a>easily </a></span>
      <span><a>and </a></span>
    </h1>
    <h1 class="hero down">
      <span><a>Style </a></span>
      <span><a>Smart.</a></span>
    </h1>
    <Button @click="schrollDown" text="Dress Up"></Button>
  </div>
  <div ref="scrollTarget" >
    <HomeSwiper class="swiper"></HomeSwiper>
  </div>
  
  

  
</template>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,200..800;1,6..72,200..800&family=Sour+Gummy:ital,wght@0,100..900;1,100..900&display=swap');
  .hero-box{
    padding-top: 32px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .hero{
    text-align: center;
    font-family: "Newsreader", serif;
    font-size: 5.5vw;
    font-weight: 300;
  }
  .hero.down{
    font-style: italic;
    color: #c07858;
    margin-top: -50px;
  }



</style>
