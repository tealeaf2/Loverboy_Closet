<template>
  <Header/>
  <div>
    <el-space :fill="true" wrap class="content">
      <el-tabs type="border-card" class="whole_table">
        <el-tab-pane label="Personal">
          <el-space :fill="true" wrap class="items">
            
            <el-card v-for="outfit in userOutfits" :key="outfit.outfit_id" class="card" lazy>
              <template #header>
                <div class="info">
                  <span class="left-span">Outfit: {{ outfit.outfit_id }}</span>
                  <span class="left-span">Price: ${{ outfit.total_price }} (USD)</span>
                  <span class="left-span">User: {{ outfit.user_id }}</span>
                  <span class="left-span">Subscribed: {{ outfit.subscribe_count }}</span>
                  <el-button class="right-span sub-button">Edit</el-button>
                </div>
              </template>
              <div @click="toggleForm(outfit)">
                <div v-for="product in outfit.products" 
                  :key="product.ProductID"
                  class="product-item"
                >
                  <el-card style="max-width: 480px">
                    <el-image style="width: 150px; height: 150px" :src="product.image_url"/>
                    <div class="desc">{{ product.productDisplayName }}</div>
                    <div class="desc">${{ product.price }}</div>
                  </el-card>
                </div>
              </div>
              <div class="footer">
                Tags: <el-tag v-for="tag in outfit.true_tags" class="tag-color" size="small">{{ tag }}</el-tag>
              </div>
            </el-card>
          </el-space>

        </el-tab-pane>
        <RecommendDrawer v-if="isFormVisible" :drawer="isFormVisible" :selectedProducts="selectedProducts" @close="closeForm"/>
        <el-tab-pane label="Saved">
          
          <el-space :fill="true" wrap class="items">
            
            <el-card v-for="outfit in subscribedOutfits" :key="outfit.outfit_id" class="card" lazy>
              <template #header>
                <div class="info">
                  <span class="left-span">Outfit: {{ outfit.outfit_id }}</span>
                  <span class="left-span">Price: ${{ outfit.total_price }} (USD)</span>
                  <span class="left-span">User: {{ outfit.user_id }}</span>
                  <span class="left-span">Subscribed: {{ outfit.subscribe_count }}</span>
                  <el-button class="right-span sub-button">Edit</el-button>
                </div>
              </template>
              <div @click="toggleForm(outfit)">
                <div v-for="product in outfit.products" 
                  :key="product.ProductID"
                  class="product-item"
                >
                  <el-card style="max-width: 480px">
                    <el-image style="width: 150px; height: 150px" :src="product.image_url"/>
                    <div class="desc">{{ product.productDisplayName }}</div>
                    <div class="desc">${{ product.price }}</div>
                  </el-card>
                </div>
              </div>
              <div class="footer">
                Tags: <el-tag v-for="tag in outfit.true_tags" class="tag-color" size="small">{{ tag }}</el-tag>
              </div>
            </el-card>
          </el-space>

        </el-tab-pane>
      </el-tabs>
    </el-space>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue"
const { $api } = useNuxtApp()
import { useNuxtApp } from '#app';
import { ElNotification } from 'element-plus'

const userOutfits = ref([]);
const isFormVisible = ref(false);
const selectedProducts = ref<any[]>([]);
const subscribedOutfits = ref<any[]>([]);

const toggleForm = (outfit: any) => {
  selectedProducts.value = outfit.products;
  isFormVisible.value = !isFormVisible.value;
};

const closeForm = () => {
  isFormVisible.value = false;
  selectedProducts.value = [];
};

onMounted(() => {
  getCreatedOutfits();
  getSubscribedOutfits();
});

const getCreatedOutfits = async() => {
  try {
    const response = await $api.get(`/user/20/outfits`);
    userOutfits.value = response.data.outfits || []; 
    console.log(userOutfits)
  } catch (error) {
    console.error("Failed to fetch outfits:", error);
  }
}

const getSubscribedOutfits = async () => {
  try {
    const response = await $api.get(`/subscribed-outfits`);
    const subscribedOutfits = response.data.outfits || [];
    console.log(subscribedOutfits);
  } catch (error) {
    console.error("Failed to fetch subscribed outfits:", error);
  }
};

</script>


<style>
.content {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 20px;
}

.desc {
  background-color: white !important;
  letter-spacing: 1px;
  align-items: center;
  font-size: 10px;
  font-weight: 350; 
}

.whole_table {
  background-color: white;
  box-shadow: var(--el-box-shadow);
  color: var(--third-color);
  letter-spacing: 1px;
  font-size: 15px;
  font-weight: 350; 
}

.card {
  background-color: var(--secondary-color);
}

.items {
  display: flex;
  flex-wrap: wrap;
  padding-left: 20px;
  padding-right: 20px;
}

.info {
  display: flex;
  color: var(--third-color);
  letter-spacing: 1px;
  align-items: center;
  font-size: 17px;
  font-weight: 350;
}

.tag-color {
  color: #838C8B;
  background-color: #ffffff;
  border-color: #838C8B;
}

</style>