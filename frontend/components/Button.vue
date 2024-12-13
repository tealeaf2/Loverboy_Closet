<script setup>
import { ref } from 'vue';
const props= defineProps(['text'])
</script>

<template>
<div class="button">{{ props.text }}</div>
</template>


<style scoped>
  .button{
    width: 150px;
    height: 50px;
    background-color: #c07858;
    border-radius: 8px;
    font-size: 17px;
    text-align: center;
    line-height: 50px;
    color: white;
    font-weight: 600;
    user-select: none;
    cursor: pointer;
  }
</style>