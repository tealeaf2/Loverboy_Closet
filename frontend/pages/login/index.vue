<script setup>
  import Header from './header.vue';
  import loginBox from './login-box.vue';
</script>
  
<template>
  <Header></Header>
  <div class="login">
    <loginBox></loginBox>
  </div>
  
</template>

<style scoped>
  .login{
    display: flex;
    padding-top: 32px;
    align-items: center;
    justify-content: center;
  }
</style>