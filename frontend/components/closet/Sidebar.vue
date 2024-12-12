<script setup>
import { ref, onMounted } from "vue"

const activeTab = ref(''); 

function handleTabClick(tab) {
  console.log('Active tab:', tab.props.label);
  activeTab.value = tab.props.label; // Update the active tab ref
}

</script>

<template>
  <el-tabs v-model="activeTab" tab-position="left" style="height: 200px" class="demo-tabs container" @tab-click="handleTabClick">
    <el-tab-pane label="All"></el-tab-pane>
    <el-tab-pane label="Apparel"></el-tab-pane>
    <el-tab-pane label="Footwear"></el-tab-pane>
    <el-tab-pane label="Accessories"></el-tab-pane>
  </el-tabs>
</template>

<style scoped>
  *{
    margin: 0;
    padding: 0;
  }
  .container{
    width: 200px;
    position: fixed;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    overflow: hidden;
    transition: 0.3s;
    z-index: 3;
    color: #ffffff;
  }
  .container:hover{
    width: 200px;
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

</style>