<template>
  <el-drawer v-model="drawer" title="I am the title" :with-header="false" @close="emitCloseEvent">
    <span>{{ selectedItem.productDisplayName }}</span>
  </el-drawer>
</template>

<script lang="ts" setup>
import { ref, defineProps, defineEmits } from 'vue';

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



</style>