<script setup>
import { ref } from 'vue';
import Header from '../header.vue';
import sidebar from './sidebar.vue';


  const isWearing = ref(false)
  const isFormVisible = ref(false)
  function wear(){
    isWearing.value=!isWearing.value
  }
  const list = ref([1,1,1,1,1])
  function toggleForm(){
    isFormVisible.value=!isFormVisible.value
  }

  function add(){

  }
</script>

<template>
  <Header></Header>
  <sidebar></sidebar>
  <div class="shell">
    <input type="checkbox" id="checkbox">
    <label for="checkbox"></label>
    <input type="text" placeholder="search" class="input" id="input">
    <div @click="add" class="add"></div>
  </div>
  <div class="container">
    <div v-for="item in list" class="box">
      <div class="top-bar"></div>
      <div class="nav">
        <i @click="wear" :class="{wearing:isWearing}" class="fi fi-rr-shirt-long-sleeve"></i>
      </div>
      <div class="pic">
        <img src="../assets/picture/shirt1.png" alt="">
      </div>
      <div class="info">
        <strong>Waffle T-Shirt</strong>
        <div class="buttons">
          
          <a href="#"><i class="fi fi-rs-trash"></i>Delete</a>
          <a href="#" @click.prevent="toggleForm"><i class="fi fi-rs-eye"></i>View</a>
        </div>
      </div>
      <div v-if="isFormVisible" class="detail-box">
        <div class="details">
          <div class="type">
            <strong>Type</strong>
            <input type="text">
          </div>
        </div>
      </div>
    </div>
    

  </div>
</template>

<style scoped>
  @import url('https://cdn-uicons.flaticon.com/2.6.0/uicons-regular-rounded/css/uicons-regular-rounded.css');
  @import url('https://cdn-uicons.flaticon.com/2.6.0/uicons-regular-straight/css/uicons-regular-straight.css');
  @import url('https://cdn-uicons.flaticon.com/2.6.0/uicons-regular-straight/css/uicons-regular-straight.css');

  *{
    box-sizing: border-box;
  }

  .shell{
    position: relative;
    width: 100vw;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 120px;
    gap: 10px;
  }

  .input{
    padding: 0;
    width: 0;
    height: 0;
    background: none;
    border: none;
    border-radius: 20px;
    outline: none;
    transition: .5s;
  }
  #checkbox{
    visibility: hidden;
  }
  [for=checkbox]{
    display: block;
    width: 70px;
    height: 70px;
    border-radius: 20px;
    background-color: var(--primary-color); /* Desired color */
    mask: url(../assets/picture/search.png) no-repeat center;
    mask-size: contain;
    -webkit-mask: url(../assets/picture/search.png) no-repeat center;
    -webkit-mask-size: contain;
  }
  #checkbox:checked~label{
    border-radius: 10px;
    background-color: var(--primary-color); /* Desired color */
    mask: url(../assets/picture/cross.png) no-repeat center;
    mask-size: contain;
    -webkit-mask: url(../assets/picture/cross.png) no-repeat center;
    -webkit-mask-size: contain;
    margin: 0 -5px;
  }
  #checkbox:checked~input{
    width: 400px;
    border-radius: 10px;
    color: black;
    visibility: visible;
    padding: 10px;
    height: 80px;
    background: none;
    border: 4px solid var(--primary-color);
    transition: .5s;
    font-size: 24px;
  }

  .add{
    display: block;
    width: 50px;
    height: 50px;
    background-color: var(--primary-color); /* Desired color */
    mask: url(../assets/picture/plus.png) no-repeat center;
    mask-size: contain;
    -webkit-mask: url(../assets/picture/plus.png) no-repeat center;
    -webkit-mask-size: contain;
  }



  .box{
    width: 266px;
    height: 390px;
    background-color: var(--secondary-color);
    box-shadow: 2px 2px 30px rgba(0,0,0,.05);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 30px 20px 30px 20px;
    border-radius: 10px;
    margin: 20px;
    position: relative;
  }
  .container{
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
  }
  .top-bar{
    width: 50%;
    height: 4px;
    position: absolute;
    left: 50%;
    top:0;
    transform: translateX(-50%);
    background-color: var(--primary-color);
  }
  .nav{
    display: flex;
    flex-direction: row-reverse;
    width: 100%;
  }
  .fi-rr-shirt-long-sleeve {
    font-size: 18px; 
    color: black;
    z-index: 1;
  }
  .fi-rr-shirt-long-sleeve.wearing{
    color: red;
  }
  .pic img{
    width: 266px;
    height: 266px;
    position: absolute;
    left: 0;
    top: 10px;

  }
  .info{
    display: flex;
    flex-direction: column;
    align-items: center;
    
  }
  strong{
    font-size: 16px;
    text-align: center;
    padding-bottom: 14px;
    line-height: 18px;
  }
  .buttons{
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 80%;
  }
  .buttons a{
    text-decoration: none;
    font-size: 18px;
    text-align: center;
    color: var(--primary-color);
    user-select: none;
    cursor: pointer;
  }
  .fi-rs-eye{
    font-size: 14px;
    margin-right: 2px;
  }
  .fi-rs-trash{
    font-size: 14px;
    margin-right: 2px;
  }
  .detail-box{
    position: absolute;
    left: 100%;
    top: 0;
    width: 390px;
    height: 390px;
    z-index: 1;
    transition:opacity 1s ease-in-out;
  }
  .details{
    position: relative;
    width: 100%;
    height: 100%;
    background-color: var(--primary-color);
    display: flex;
    flex-direction: column;
    padding: 20px;
  }
  .type{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .type strong{
    font-size: 30px;
    line-height: 1px;
  }


</style>