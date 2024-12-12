<!-- <template>
  <el-dialog v-model="openEdit" title="" width="1000" @close="emitCloseEvent" class="edit-box">
    <el-row>
      <el-col :span="12" class="left-col">
        <el-card class="design" style="width: 100%;">
          <div class="product-container" v-for="product in outfit" :key="product.ProductID">
            <div class="product-content">
              <div class="upload-mimic">
                <img :src="product.image_url" alt="Product image" class="product-image" />
                <div class="hover-overlay">
                  <el-icon style="margin: 5px;">
                    <ZoomIn />
                  </el-icon>
                  <el-icon style="margin: 5px;" @click="removeProduct(product.ProductID)">
                    <Delete />
                  </el-icon>
                </div>
              </div>
              <div class="product-info">
                <div>{{ product.productDisplayName }}</div>
                <div>{{ product.masterCategory }}</div>
                <div>{{ product.usage }}</div>
                <div>{{ product.year }}</div>
                <div>${{ product.price }} (USD)</div>
              </div>
            </div>
          </div>
          <el-tag v-for="tag in outfitTags" :key="tag" class="tag-color" size="small">{{ tag }}</el-tag>
        </el-card>
      </el-col>
      <el-col :span="12" class="right-col">
        Clothing Options
      </el-col>
    </el-row>
    <div class="edit-footer">
      <el-button class="cancel-button" @click="closeEdit">Cancel</el-button>
      <el-button class="confirm-button" primary @click="">
        Save
      </el-button>
    </div>
  </el-dialog>
</template> -->

<template>
  <el-dialog v-model="openEdit" title="" width="1000" @close="emitCloseEvent" class="edit-box">
    <el-row>
      <el-col :span="12" class="left-col">
        <el-card class="design" style="width: 100%;">
          <div class="product-container" v-for="category in categories" :key="category.name">
            <div class="product-content">
              <div class="upload-mimic">
                <img :src="category.product ? category.product.image_url : ''" alt="Product image" class="product-image" />
                <div class="hover-overlay">
                  <el-icon style="margin: 5px;">
                    <ZoomIn />
                  </el-icon>
                  <el-icon style="margin: 5px;" @click="removeProduct(category)">
                    <Delete />
                  </el-icon>
                </div>
              </div>
              <div class="product-info">
                <div>{{ category.product ? category.product.productDisplayName : category.name }}</div>
                <div>{{ category.product ? category.product.masterCategory : '' }}</div>
                <div>{{ category.product ? category.product.usage : '' }}</div>
                <div>{{ category.product ? category.product.year : '' }}</div>
                <div>{{ category.product ? `$${category.product.price} (USD)` : '' }}</div>
              </div>
            </div>
          </div>
          <el-tag v-for="tag in outfitTags" :key="tag" class="tag-color" size="small">{{ tag }}</el-tag>
        </el-card>
      </el-col>
      <el-col :span="12" class="right-col">
        Clothing Options
      </el-col>
    </el-row>
    <div class="edit-footer">
      <el-button class="cancel-button" @click="closeEdit">Cancel</el-button>
      <el-button class="confirm-button" primary @click="">Save</el-button>
    </div>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { ZoomIn, Delete } from '@element-plus/icons-vue'

const props = defineProps<{
  edit: boolean;
  selectedOutfit: any;
}>();

type Product = {
  ProductID: number;
  articleType: string;
  baseColour: string;
  category: string;
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

type Category = {
  name: string;
  product: Product | null;
};

const categories = ref<Category[]>([
  { name: 'Topwear', product: null },
  { name: 'Bottomwear', product: null },
  { name: 'Accessory', product: null },
  { name: 'Footwear', product: null },
]);

const openEdit = ref(props.edit);
const outfit = ref(props.selectedOutfit.products);
const outfitTags = ref(props.selectedOutfit.true_tags);

onMounted(() => {
  updateOutfitCategories();
})

const removeProduct = (category: any) => {
  console.log(category);
  // const category = categories.value.find(cat => cat.name === categoryName);
  // if (category && category.product) {
  //   outfit.value = outfit.value.filter(product => product.ProductID !== category.product.ProductID);
  //   category.product = null;
  //   updateTags();
  // }
};

const updateOutfitCategories = () => {
  categories.value.forEach(category => category.product = null);

  outfit.value.forEach((product: Product) => {
    console.log(product);
    switch (product.category.toLowerCase()) {
      case 'shirt':
        categories.value.find(cat => cat.name === 'Topwear')!.product = product; 
        break;
      case 'outerwear':
        categories.value.find(cat => cat.name === 'Topwear')!.product = product; 
        break;
      case 'pant':
        categories.value.find(cat => cat.name === 'Bottomwear')!.product = product;
        break;
      case 'accessory':
        categories.value.find(cat => cat.name === 'Accessory')!.product = product;
        break;
      case 'shoe':
        categories.value.find(cat => cat.name === 'Footwear')!.product = product;
        break;
      default:
        break;
    }
  });
};

const updateTags = () => {
  const tags = new Set();
  outfit.value.forEach(product => {
    product.season_style && Object.keys(product.season_style).forEach(season => {
      if (product.season_style[season]) {
        tags.add(season);
      }
    });
  });
  outfitTags.value = Array.from(tags);
};


const closeEdit = () => {
  openEdit.value = false;
};

const emit = defineEmits<{ (event: 'close'): void }>();

const emitCloseEvent = () => {
  setTimeout(() => {
    emit('close');
  }, 300);
};
</script>

<style>
.edit-box {
  background-color: var(--secondary-color);
}

.product-info {
  color: var(--third-color);
  font-size: 12px;
  font-weight: 350;
  width: 300px; 
}

.product-content {
  display: flex;
  gap: 10px;
}

.upload-mimic {
  width: 150px;
  height: 150px;
  border: 2px dashed #d9d9d9;
  border-radius: 6px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #fafafa;
  overflow: hidden;
  cursor: pointer;
  transition: border-color 0.3s;
}

.upload-mimic:hover {
  border-color: var(--primary-color);
  /* Highlight border on hover */
}

.product-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  justify-content: space-between;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 10px;
  opacity: 0;
  transition: opacity 0.3s;
}

.upload-mimic:hover .hover-overlay {
  opacity: 1;
}

.hover-overlay .el-icon {
  color: white;
  font-size: 24px;
  cursor: pointer;
  transition: transform 0.2s;
}

.hover-overlay .el-icon:hover {
  transform: scale(1.2);
}

.product-container {
  margin-bottom: 16px;
}

.cancel-button {
  border: 1px solid #c07858;
  color: #c07858;
}

.confirm-button {
  background-color: #c07858;
  color: white;
}

.edit-footer {
  display: flex;
  justify-content: flex-end;
}

.left-col,
.right-col {
  display: flex;
  align-items: center;
  height: 100%;
}
</style>
