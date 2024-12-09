<script setup>
  import { ref,defineProps } from 'vue'; 
  // important!!!! import ref every time, or nothing shows up!!!!!
  const isFlipped= ref(false);
  function flip(){
    isFlipped.value=!isFlipped.value
  }
  const props= defineProps(['outfit','photo'])



</script>

<template>
  <div @click="flip" class="card-container">
    <div class="cover" :class="[isFlipped?'flipped':'origin']">
      <img :src="props.photo" alt="">
    </div>
    <div class="back" :class="[!isFlipped?'flipped':'origin']" >
      <img :src="props.outfit" alt="">
    </div>
  </div> 
</template>

<style scoped>
.card-container{
  width: 300px;
  height: 500px;
  margin-left: 1%;
  position: relative;
  cursor: pointer;
  perspective: 1000px;
  overflow: hidden;
  border-radius: 50px;
}
.cover, .back{
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  text-align: center;
  display: flex;
  align-items: center;
  justify-items: center;
  transition: transform .25s ease-in-out
}
.cover.origin{
  transform: rotateY(0deg);
}
.flipped.cover{
  transform: rotateY(180deg);
}
.origin.back{
  transform: rotateY(0deg);
}
.flipped.back{
  transform: rotateY(-180deg);
}

img{
  object-fit: contain;
  max-width: 100%;
  max-height: 100%;
}
</style>
