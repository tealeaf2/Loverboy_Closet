<template>
  <el-dialog v-model="openDialog" title="" width="1000" @close="emitCloseEvent" class="detail-box">
    <div
      class="outfit" 
    >
      <el-card v-for="product in outfit.products" style="max-width: 480px" class="product-card">
        <div style="display: flex; justify-content: flex-end;">
          <el-button v-if="!product.is_subscribed" :icon="Plus" circle @click="addProduct(product)"/>
          <el-button v-if="product.is_subscribed" :icon="Minus" circle @click="deleteProduct(product)"/>
        </div>

        <el-image style="width: 150px; height: 200px" :src="product.image_url"/>
        <div class="desc">Name: {{ product.productDisplayName }}</div>
        <div class="desc">Price: ${{ product.price }} (USD)</div>
        <div class="desc">Category: {{ product.masterCategory }}</div>
        <div class="desc">Usage: {{ product.usage }}</div>
        <div class="desc">Color: {{ product.baseColour }}</div>
          <el-tag v-for="tag in tags(product.season_style)" 
            :key="tag"
            class="tag-color" 
            size="small">
            {{ tag }}
          </el-tag>
      </el-card>
    </div>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
const { $api, $authApi } = useNuxtApp()
import { useNuxtApp } from '#app';
import { Plus, Minus } from '@element-plus/icons-vue'
import { ElNotification } from 'element-plus';

const props = defineProps<{
  dialog: boolean;
  selectedOutfit: any;
}>();
onMounted(() => {
  checkOutfit();
});

const openDialog = ref(props.dialog);
const outfit = ref(props.selectedOutfit);

const deleteProduct = async (product: any) => {
  const user = 20;
  try {
    const response = await $authApi.delete(`/user/products/${product.ProductID}`);
    if (response.status === 200) {
      console.log(`Product ${product.ProductID} successfully removed from user ${user}`);
      product.is_subscribed = false;
    } else {
      console.error('Failed to delete the product:', response.data);
    }
  } catch (error) {
    console.error('Error fetching products:', error);
  }
};

const addProduct = async (product: any) => {
  try {
    const response = await $authApi.post('/products', {
      products: [
        {
          ProductID: product.ProductID,
          articleType: product.articleType,
          baseColour: product.baseColour,
          favorite: product.favorite,
          gender: product.gender,
          image_url: product.image_url,
          masterCategory: product.masterCategory,
          price: product.price,
          productDisplayName: product.productDisplayName,
          season_style: product.season_style,
          subCategory: product.subCategory,
          usage: product.usage,
          year: product.year,
        }
      ],
    });
    product.is_subscribed = true;
    ElNotification({
      title: 'Success',
      message: 'Product added successfully',
      type: 'success',
    });

    console.log('Product added successfully:', response.data);

  } catch (error) {
    console.error('Error adding product:', error);
  }
};

const checkOutfit = async() => {
  try {
    const response = await $authApi.get(`/check-outfit/${outfit.value.outfit_id}`);
    outfit.value = response.data.outfits;

  } catch (error) {
    console.error('Error while checking outfit:', error);
  }
}

const tags = (seasonStyle: any) => {
  return Object.keys(seasonStyle).filter(tag => seasonStyle[tag] === true);
};

const emit = defineEmits<{ (event: 'close'): void }>();
const emitCloseEvent = () => {
  setTimeout(() => {
    emit('close');
  }, 300);
};

</script>

<style>
.detail-box {
  background-color: var(--secondary-color);
}
.outfit {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  gap: 20px;
}

.product-card {
  width: 48%; 
  box-sizing: border-box;
}

</style>