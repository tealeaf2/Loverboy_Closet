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
                  <el-button class="right-span delete-button" @click="deleteOutfit(outfit.outfit_id)">Delete</el-button>
                </div>
              </template>
              <div @click="">
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
        <el-tab-pane label="Saved">
          <el-space :fill="true" wrap class="items">
            <el-card v-for="outfit in subscribedOutfits" :key="outfit.outfit_id" class="card" lazy>
              <template #header>
                <div class="info">
                  <span class="left-span">Outfit: {{ outfit.outfit_id }}</span>
                  <span class="left-span">Price: ${{ outfit.total_price }} (USD)</span>
                  <span class="left-span">User: {{ outfit.user_id }}</span>
                  <span class="left-span">Subscribed: {{ outfit.subscribe_count }}</span>
                  <el-button class="right-span sub-button" @click="unsaveOutfit(outfit.outfit_id)">Unsubscribe</el-button>
                </div>
              </template>
              <div @click="toggleDetail(outfit)">
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
                <div class="footer">
                  Tags: <el-tag v-for="tag in outfit.true_tags" :key="tag" class="tag-color" size="small">{{ tag }}</el-tag>
                </div>
              </div>
            </el-card>
          </el-space>

          <OutfitDetail v-if="openDialog" :dialog="openDialog" :selectedOutfit="selectedOutfit" @close="closeForm"/>

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

const userOutfits = ref<any[]>([]);
const subscribedOutfits = ref<any[]>([]);
const selectedOutfit = ref<any[]>([]);
const openDialog = ref(false);

onMounted(() => {
  getCreatedOutfits();
  getSubscribedOutfits();
});

const toggleDetail = (outfit: any) => {
  selectedOutfit.value = outfit;
  openDialog.value = !openDialog.value;
}

const closeForm = () => {
  openDialog.value = false;
  selectedOutfit.value = [];
};


const deleteOutfit = async(outfit_id: number) => {
  try {
    const response = await $api.delete(`/outfits/${outfit_id}`)

    userOutfits.value = userOutfits.value.filter(outfit => outfit.outfit_id !== outfit_id);
    ElNotification({
      title: 'Success',
      message: `Successfully deleted!`,
      type: 'success',
    }); 
  } catch (error) {
    console.error("Failed to delete:", error);
  }
}


const unsaveOutfit = async(outfitId: number) => {
  try {
    const response = await $api.post('/unsave_outfit', {
      user_id: 20, // TODO: Replace
      outfit_id: outfitId
    });
    
    ElNotification({
      title: 'Success',
      message: `Successfully unsubscribed!`,
      type: 'success',
    });

    subscribedOutfits.value = subscribedOutfits.value.filter(outfit => outfit.outfit_id !== outfitId);

  } catch (error) {
    console.error("Failed to unsubscribe:", error);
  }
};


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
    subscribedOutfits.value = response.data.subscribed_outfits;
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

.left-span{
  margin-right: 20px;
}

.right-span{
  margin-left: auto;
}

.tag-color {
  color: #838C8B;
  background-color: #ffffff;
  border-color: #838C8B;
}

.sub-button {
  border: 1px solid #c07858;
  border-radius: 4px;
  font-size: 17px;
  text-align: center;
  line-height: 50px;
  color: #c07858;
}

.delete-button {
  background-color: #c07858;
  border-radius: 4px;
  font-size: 17px;
  text-align: center;
  line-height: 50px;
  color: white;
}

</style>