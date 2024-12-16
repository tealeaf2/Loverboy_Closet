<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'

const router = useRouter()

const isAuthenticated = ref(false);

onMounted(() => {
  if (process.client) {
    const token = localStorage.getItem('token');
    isAuthenticated.value = !!token;
  }
});

const handleSignOut = () => {
  localStorage.removeItem('token');
  isAuthenticated.value = false;
  router.push('/')
};
</script>

<template>
  <el-page-header icon="">
    <template #icon>
    </template>
    <template #title>
      <NuxtLink to='/' class="header-left">
        <div class="logo-pic">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="-0.008 -0.1 283.36 112" width="373.97" height="147.81">
            <path
              d="M282.18,111.9H11.94a11.94,11.94,0,0,1-4.2-23.12l138-51.94V28.62a1.28,1.28,0,0,1,1.28-1.29A12.38,12.38,0,1,0,135.2,11.39a6.13,6.13,0,0,0-.16,1.16c-.12,1.3-.3,3.27-2.1,3.66a1.28,1.28,0,0,1-.55-2.51,13.2,13.2,0,0,1,.09-1.39,8.38,8.38,0,0,1,.26-1.66,15,15,0,1,1,15.61,19.2v7.88a1.3,1.3,0,0,1-.84,1.2L8.64,91.19a9.37,9.37,0,0,0,3.3,18.14H282.18a1.29,1.29,0,0,1,0,2.57Z"
              style="fill: rgb(35, 31, 32);"></path>
          </svg>
        </div>
        <div class="brand">
          <svg width="458" height="70" viewBox="0 0 458 70" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path
              d="M0.672 69V0.359997H5.28V64.776H36.864V69H0.672ZM72.822 69.96C63.926 69.96 56.47 66.856 50.454 60.648C44.438 54.44 41.43 46.856 41.43 37.896C41.43 28.872 44.438 21.256 50.454 15.048C56.47 8.84 63.926 5.736 72.822 5.736C81.718 5.736 89.174 8.84 95.19 15.048C101.206 21.256 104.214 28.872 104.214 37.896C104.214 46.856 101.206 54.44 95.19 60.648C89.174 66.856 81.718 69.96 72.822 69.96ZM72.822 9.672C65.142 9.672 58.742 12.392 53.622 17.832C48.566 23.272 46.038 29.96 46.038 37.896C46.038 45.768 48.566 52.424 53.622 57.864C58.742 63.24 65.142 65.928 72.822 65.928C80.566 65.928 86.966 63.24 92.022 57.864C97.078 52.424 99.606 45.768 99.606 37.896C99.606 29.96 97.078 23.272 92.022 17.832C86.966 12.392 80.566 9.672 72.822 9.672ZM141.653 55.944L162.485 6.696H167.093L140.309 69.384H137.717L110.933 6.696H115.733L139.253 62.088C139.573 61.128 140.373 59.08 141.653 55.944ZM179.801 69V6.696H208.889V10.536H184.217V33.192H206.489V36.936H184.217V64.968H209.849V69H179.801ZM227.52 69V6.984C233.024 6.536 237.696 6.31199 241.536 6.31199C247.424 6.31199 252.288 7.848 256.128 10.92C259.968 13.928 261.888 18.248 261.888 23.88C261.888 27.656 260.8 31.144 258.624 34.344C256.448 37.544 253.984 40.136 251.232 42.12C258.848 52.232 263.552 58.28 265.344 60.264C268.992 64.04 272.96 66.184 277.248 66.696L277.152 69.672C273.568 69.608 270.656 69.096 268.416 68.136C266.176 67.112 263.936 65.416 261.696 63.048C259.52 60.68 254.688 54.312 247.2 43.944C242.016 43.944 236.928 43.784 231.936 43.464V69H227.52ZM244.8 40.296C247.296 40.296 249.984 38.632 252.864 35.304C255.744 31.976 257.184 28.104 257.184 23.688C257.184 19.272 255.68 15.912 252.672 13.608C249.664 11.304 245.76 10.152 240.96 10.152C238.4 10.152 235.392 10.28 231.936 10.536V39.816C236.544 40.136 240.832 40.296 244.8 40.296ZM285.83 6.984C290.374 6.6 295.046 6.408 299.846 6.408C304.646 6.408 308.742 7.56 312.134 9.86399C315.59 12.168 317.318 15.528 317.318 19.944C317.318 23.272 316.422 26.344 314.63 29.16C312.838 31.976 310.662 34.12 308.102 35.592C312.262 36.808 315.718 38.984 318.47 42.12C321.222 45.256 322.598 48.808 322.598 52.776C322.598 58.28 320.838 62.44 317.318 65.256C313.862 68.072 308.966 69.48 302.63 69.48C296.294 69.48 290.694 69.256 285.83 68.808V6.984ZM294.566 37.512L290.246 37.608V65.16C292.998 65.416 297.446 65.544 303.59 65.544C307.75 65.544 311.174 64.392 313.862 62.088C316.614 59.72 317.99 56.776 317.99 53.256C317.99 49.672 316.614 46.568 313.862 43.944C311.174 41.256 307.654 39.368 303.302 38.28C301.062 37.768 298.15 37.512 294.566 37.512ZM312.998 19.848C312.998 16.712 311.686 14.312 309.062 12.648C306.438 10.92 303.302 10.056 299.654 10.056C296.006 10.056 292.87 10.152 290.246 10.344V33.864C295.814 33.864 300.262 34.024 303.59 34.344C306.086 33 308.262 31.048 310.118 28.488C312.038 25.864 312.998 22.984 312.998 19.848ZM367.103 69.96C358.207 69.96 350.751 66.856 344.735 60.648C338.719 54.44 335.711 46.856 335.711 37.896C335.711 28.872 338.719 21.256 344.735 15.048C350.751 8.84 358.207 5.736 367.103 5.736C375.999 5.736 383.455 8.84 389.471 15.048C395.487 21.256 398.495 28.872 398.495 37.896C398.495 46.856 395.487 54.44 389.471 60.648C383.455 66.856 375.999 69.96 367.103 69.96ZM367.103 9.672C359.423 9.672 353.023 12.392 347.903 17.832C342.847 23.272 340.319 29.96 340.319 37.896C340.319 45.768 342.847 52.424 347.903 57.864C353.023 63.24 359.423 65.928 367.103 65.928C374.847 65.928 381.247 63.24 386.303 57.864C391.359 52.424 393.887 45.768 393.887 37.896C393.887 29.96 391.359 23.272 386.303 17.832C381.247 12.392 374.847 9.672 367.103 9.672ZM433.711 69H429.391V46.728L405.871 6.696H411.151L429.295 37.608C430.703 40.424 431.503 41.928 431.695 42.12C432.079 41.288 432.879 39.816 434.095 37.704L452.239 6.696H457.231L433.711 46.92V69Z"
              fill="black" />
          </svg>
        </div>
      </NuxtLink>
    </template>
    <template #content>
      <div class="nav">
        <NuxtLink to="/closet">Closet</NuxtLink>
        <NuxtLink to="/recommend">Recommend</NuxtLink>
        <NuxtLink to="/outfits">Outfits</NuxtLink>
      </div>
    </template>

    <template #extra>
      <div class="buttons">
        <el-button v-if="isAuthenticated" class="login-button" @click="handleSignOut" style="margin-right: 10px;">Sign Out</el-button>
        <NuxtLink v-else to="/login" style="margin-right: 10px;">
          <el-button class="sign-up-button">Login</el-button>
        </NuxtLink>
      </div>
    </template>
  </el-page-header>

</template>

<style scoped>
.header {
  min-width: 90vw;
  display: flex;
  justify-content: space-between;
  padding: 0 40px;
  align-items: center;
}

.header-left {
  display: flex;
  width: 30%;
  align-items: center;
  gap: 1vw;
}

.logo-pic svg {
  width: 6vw;
}

.logo-pic svg path {
  stroke-width: 4;
}

.brand svg {
  width: 15.5vw;
}

.brand svg path {
  fill: transparent;
  stroke: black;
  stroke-dasharray: 300;
  animation: brandAnimation 4s ease-in-out alternate infinite;
}

.header-right {
  display: flex;
  justify-content: space-between;
  width: 36%;
}

.nav{
    display: flex;
    align-items: center;
    gap:34px; 
  }
  .nav a{
    font-size: 17px;
    font-weight: 350;
    text-decoration: none; 
    letter-spacing: 1px;
    color: #838C8B;
  }

.buttons {
  display: flex;
  gap: 20px;
}

.login-button {
  width: 100px;
  height: 50px;
  border: 1px solid #c07858;
  border-radius: 8px;
  font-size: 17px;
  text-align: center;
  line-height: 50px;
  color: #c07858;
}

.sign-up-button {
  width: 130px;
  height: 50px;
  background-color: #c07858;
  border-radius: 8px;
  font-size: 17px;
  text-align: center;
  line-height: 50px;
  color: white;
}

@keyframes brandAnimation {
  from {
    stroke-dashoffset: 300;
  }

  to {
    stroke-dashoffset: 0;
  }
}
</style>
