<script setup>
  import { computed, ref } from 'vue';
  import card from './card.vue';

  const list= ref([
    {
    photo:'./assets/picture/photo1.jpg',
    outfit:'./assets/picture/outfit1.jpg'
    },
    {
    photo:'./assets/picture/photo2.jpg',
    outfit:'./assets/picture/outfit2.jpg'
    },
    {
    photo:'./assets/picture/photo3.jpg',
    outfit:'./assets/picture/outfit3.jpg'
    },
    {
    photo:'./assets/picture/photo4.jpg',
    outfit:'./assets/picture/outfit4.jpg'
    },
  ])

  const dupList = computed(() => [...list.value, ...list.value])


</script>

<template>
  <div class="swiper">
    <div class="swiper-content">
      <card v-for="(item,index) in dupList" class="swiper-item" :outfit="item.outfit" :photo="item.photo"></card>
    </div>
  </div>
</template>

<style scoped>
.swiper{
  margin-left: -18px;
  margin-top: 200px;
  width: 100vw;
  height: 730px;
  position: relative;
  overflow: hidden;
}
.swiper-content{
  position: absolute;
  left: 0;
  display: flex;
  flex-wrap: nowrap;
  animation: scroll 40s normal linear infinite;
  transition: animation-play-state 0.5s ease;
} 
.swiper-item{
  height: 730px;
  width: 600px;
}
/* .swiper-content:hover {
  animation-play-state: paused;
} */
@keyframes scroll {
  to {
    transform: translateX(-50%);
  }
}

</style>