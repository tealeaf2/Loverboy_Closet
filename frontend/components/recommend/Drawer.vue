<template>
  <el-drawer 
    class="content" 
    v-model="localDrawer" 
    title="I am the title" 
    :with-header="false" 
    @close="emitCloseEvent"
  >
    <el-card v-for="product in products" class="inside_card">
      <el-button :icon="Edit" circle @click="addProduct(product)"/>
      <img :src="product.image_url" />
        <el-descriptions direction="vertical" :column="1">
          <el-descriptions-item label="Name:">{{ product.productDisplayName }}</el-descriptions-item>
          <el-descriptions-item label="Type:">{{ product.articleType }}</el-descriptions-item>
          <el-descriptions-item label="Price:">
            ${{ product.price }} (USD)
          </el-descriptions-item>
        </el-descriptions>
    </el-card>
  </el-drawer>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';
import { Edit } from '@element-plus/icons-vue'
import { useNuxtApp } from '#app';
import { ElNotification } from 'element-plus';
const { $api, $authApi } = useNuxtApp()
const props = defineProps<{
  drawer: boolean;
  selectedProducts: any;
}>();

const emit = defineEmits<{ (event: 'close'): void }>();
const localDrawer = ref(props.drawer);
const products = ref(props.selectedProducts)
const emitCloseEvent = () => {
  setTimeout(() => {
    emit('close');
  }, 300);
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

    ElNotification({
      title: 'Success',
      message: 'Product added successfully',
      type: 'success',
    });

    console.log('Product added successfully:', response.data);

  } catch (error) {
    // Handle errors
    console.error('Error adding product:', error);

    ElNotification({
      title: 'Error',
      message: 'Failed to add product. Please try again.',
      type: 'error',
    });
  }
};
</script>

<style>
.inside_card {
  display: flex;
  flex-direction: column;
  max-width: 100%;
  box-sizing: border-box;
  background-color: white;
  overflow: hidden;
}

.inside_card img {
  max-width: 100%;
  height: auto;
  object-fit: contain;
}

.inside_card p {
  max-width: 100%;
  text-align: center;
  font-size: 0.5rem;
}

.content {
  background-color: var(--secondary-color);
}
</style>
  