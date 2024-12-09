<script setup>
  import { computed, ref } from 'vue';

  const list= ref([
    {
    photo:'/picture/photo1.jpg',
    outfit:'/picture/outfit1.jpg'
    },
    {
    photo:'/picture/photo2.jpg',
    outfit:'/picture/outfit2.jpg'
    },
    {
    photo:'/picture/photo3.jpg',
    outfit:'/picture/outfit3.jpg'
    },
    {
    photo:'/picture/photo4.jpg',
    outfit:'/picture/outfit4.jpg'
    },
  ])

  const dupList = computed(() => [...list.value, ...list.value])


</script>

<template>
  <div class="swiper">
    <div class="swiper-content">
      <HomeCard v-for="(item,index) in dupList" class="swiper-item" :outfit="item.outfit" :photo="item.photo"></HomeCard>
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