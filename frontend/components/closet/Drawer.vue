<template>
  <el-drawer class="desc" v-model="drawer" title="I am the title" :with-header="false" @close="emitCloseEvent">
    <el-card class="card">
      <img :src="selectedItem.image_url" />
      <p>{{ selectedItem.productDisplayName }}</p>
      <template #footer>
        <div class="content">
          <el-descriptions direction="vertical" :column="1">
            <el-descriptions-item label="Type:">{{ selectedItem.articleType }}</el-descriptions-item>
            <el-descriptions-item label="Usage:">{{ selectedItem.usage }}</el-descriptions-item>
            <el-descriptions-item label="Tags:">
              <el-tag v-for="tag in listTags" class="tag-color" size="small">{{ tag }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="Price:">
              ${{ selectedItem.price }} (USD)
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </template>
    </el-card>
  </el-drawer>
</template>

<script lang="ts" setup>
import { ref, defineProps, computed } from 'vue';

interface Product {
  ProductID: number;
  articleType: string;
  baseColour: string;
  favorite: boolean;
  gender: string;
  image_url: string;
  masterCategory: string;
  price: number;
  productDisplayName: string;
  season_style: {
    Business: boolean;
    Casual: boolean;
    Fall: boolean;
    Sport: boolean;
    Spring: boolean;
    Summer: boolean;
    Winter: boolean;
  };
  subCategory: string;
  usage: string;
  year: number;
}

const listTags = computed(() => {
  if (!props.selectedItem) return [];
  const { season_style } = props.selectedItem;

  return Object.keys(season_style).filter((key) => season_style[key]); 
})

const emit = defineEmits<{ (event: 'close'): void }>();

const props = defineProps<{
  drawer: boolean;
  selectedItem: Product | null;
}>();

const drawer = ref(props.drawer);
const emitCloseEvent = () => {
  setTimeout(() => {
    emit('close');
  }, 300);
};
</script>

<style>
.desc {
  background-color: var(--secondary-color);
}

.card {
  display: flex;
  flex-direction: column;
  max-width: 100%;
  box-sizing: border-box;
}

.card img {
  max-width: 100%;
  height: auto;
  object-fit: contain;
}

.card p {
  max-width: 100%;
  text-align: center;
  font-size: 0.5rem;
  color: var(--third-color);
}

.content {
  background-color: var(--secondary-color);
  width: 100%;
}

.tag-color {
  color: #838C8B;
  background-color: #ffffff;
  border-color: #838C8B;
  margin-right: 8px;
}
</style>