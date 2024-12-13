<template>
  <Header />

  <div v-if="isClient" class="tags">
    <el-select 
      size="small"
      placeholder="+ New Tag"
      style="width: 200px; margin-right: 20px"
      @change="handleSelect"
    >
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      /> 
    </el-select>

    <el-tag 
      v-for="tag in dynamicTags" 
      :key="tag" 
      closable 
      :disable-transitions="false" 
      @close="handleClose(tag)"
      class="tag-color">
      {{ tag }}
    </el-tag>
  </div>

  <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :size="size"
    layout="prev, pager, next, jumper" :total="filteredOutfits.length" class="demo-pagination-block"/>

  <el-space :fill="true" wrap class="items">
      <el-card v-for="outfit in paginatedClothes" :key="outfit.outfit_id" class="card" lazy>
        <template #header>
          <div class="info">
            <span class="left-span">Outfit: {{ outfit.outfit_id }}</span>
            <span class="left-span">Price: ${{ outfit.total_price }} (USD)</span>
            <span class="left-span">User: {{ outfit.user_id }}</span>
            <span class="left-span">Subscribed: {{ outfit.subscribe_count }}</span>
            <el-button class="right-span sub-button" @click="saveOutfit(outfit)">Subscribe</el-button>
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
  <RecommendDrawer v-if="isFormVisible" :drawer="isFormVisible" :selectedProducts="selectedProducts" @close="closeForm"/>

</template>


<script lang="ts" setup>
import { onMounted, ref, computed } from 'vue'
import options from './options'
const { $api } = useNuxtApp()
import { useNuxtApp } from '#app';
import { ElNotification, ComponentSize } from 'element-plus'

const isClient = ref(false);
const recommendations = ref<any[]>([]);
const isFormVisible = ref(false);
const selectedProducts = ref<any[]>([]);
const currentPage = ref(1)
const pageSize = ref(15);
const size = ref<ComponentSize>('default')

onMounted(() => {
  getRecommendations();
  isClient.value = true;
});

const dynamicTags = ref<string[]>([])

const paginatedClothes = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredOutfits.value.slice(start, end);
});

const toggleForm = (outfit: any) => {
  selectedProducts.value = outfit.products;
  isFormVisible.value = !isFormVisible.value;
};

const closeForm = () => {
  isFormVisible.value = false;
  selectedProducts.value = [];
};


const saveOutfit = async (outfit: any) => {
  try {
    const payload = {
      user_id: 20,
      outfit_id: outfit.outfit_id
    };

    const response = await $api.post('/save_outfit', payload);
    getRecommendations();
    ElNotification({
      title: 'Success',
      message: 'Outfit added successfully',
      type: 'success',
    });
  } catch (error) {
    console.error(error)
  }
};

const filteredOutfits = computed(() => {
  if (dynamicTags.value.length === 0) {
    return recommendations.value;
  }
  const tagsToFilter = dynamicTags.value.filter(tag => tag !== 'Cheap' && tag !== 'Expensive');

  let filtered = recommendations.value.filter(outfit => {
    return tagsToFilter.every(tag => outfit.true_tags.includes(tag));
  });

  if (dynamicTags.value.includes('Cheap')) {
    filtered.sort((a, b) => a.total_price - b.total_price);
  } else if (dynamicTags.value.includes('Expensive')) {
    filtered.sort((a, b) => b.total_price - a.total_price);
  }

  return filtered;
})

const getRecommendations = async () => {
  try {
    const response = await $api.get('/outfits');
    const outfits = response.data.outfits;

    if (outfits && outfits.length > 0) {
      recommendations.value = outfits;
    } else {
      recommendations.value = [];
    }
  } catch (error) {

  }
}

const handleClose = (tag: string) => {
  dynamicTags.value.splice(dynamicTags.value.indexOf(tag), 1)
}
const handleSelect = (value: string) => {
  if (value && !dynamicTags.value.includes(value)) {
    dynamicTags.value.push(value)
  }
}
</script>

<style>
.card {
  background-color: var(--secondary-color);
}

.footer {
  color: var(--third-color);
  letter-spacing: 1px;
  font-size: 15px;
  font-weight: 350; 
}

.desc {
  background-color: white !important;
  letter-spacing: 1px;
  align-items: center;
  font-size: 10px;
  font-weight: 350; 
}

.product-item {
  flex-wrap: wrap;
  display: flex;
  display: inline-flex;
  margin: 10px;
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

.tags {
  padding-left: 20px;
  padding-right: 20px;
}

.tag-color {
  color: #838C8B;
  background-color: #ffffff;
  border-color: #838C8B;
}

.items {
  padding-left: 20px;
  padding-right: 20px;
}

.sub-button {
  border: 1px solid #c07858;
  border-radius: 4px;
  font-size: 17px;
  text-align: center;
  line-height: 50px;
  color: #c07858;
}

.demo-pagination-block {
  margin: 10px;
  color: var(--third-color);
  --el-pagination-bg-color: var(--secondary-color);
  --el-pagination-button-disabled-bg-color: var(--secondary-color); 
}
</style>
