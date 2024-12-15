<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
onMounted(() => {
  const token = localStorage.getItem('token')
  
  if (token) {
    router.push('/closet')
  }
})
</script>
  
<template>
  <Header></Header>
  <div class="login">
    <LoginBox></LoginBox>
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