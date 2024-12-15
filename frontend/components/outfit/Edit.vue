<template>
  <el-dialog v-model="openEdit" title="" width="1000" @close="emitCloseEvent" class="edit-box" :before-close="handleClose">
    <el-row>
      <el-col :span="12" class="left-col">
        <el-card class="design" style="width: 100%;">
          <div class="product-container" v-for="category in categories" :key="category.name">
            <div class="product-content">
              <div 
                :class="['upload-mimic', { 'selected': category.name === selectedCategory }]" 
                @click="category.product ? null : selectTable(category.name)"
              >
                <img v-if="category.product" :src="category.product.image_url" alt="Product image" class="product-image" />
                <div v-else>
                  <el-icon> <Plus /> </el-icon>
                </div>
                <div v-if="category.product" class="hover-overlay">
                  <el-icon @click="removeProduct(category)">
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
        <el-tabs class="demo-tabs" type="card" style="margin-left: 20px; width: 100%">
          <el-tab-pane label="My Closet">
            <el-input
              v-model="input"
              style="width: 100%; margin-bottom: 10px"
              placeholder="Search Clothes"
              :prefix-icon="Search"
            />
            <div class="product-images" style="height: 510px; overflow-y: auto;">
              <el-space
                fill
                wrap
                :fill-ratio="30"
                direction="horizontal"
                style="width: 100%"
              >
              <div v-for="product in filteredClothes" :key="product.ProductID" class="image-item" @click="addProduct(product)">
                <el-card>
                  <el-image :src="product.image_url" fit="contain"/>
                  <div class="font">{{ product.productDisplayName }}</div>
                </el-card>
              </div>
              </el-space>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-col>

    </el-row>
    <div class="edit-footer">
      <el-button class="cancel-button" @click="closeEdit()">Cancel</el-button>
      <el-button class="confirm-button" primary @click="uploadOutfit()">Save</el-button>
    </div>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue';
import { ZoomIn, Delete, Plus, Search } from '@element-plus/icons-vue'
import { ElNotification } from 'element-plus'
const { $api, $authApi } = useNuxtApp();
import { useNuxtApp } from '#app';

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

const clothes = ref<Product[]>([])
const filteredClothes = ref<Product[]>([])
const input = ref('')

onMounted(() => {
  updateOutfitCategories();
  getData();
})

const categories = ref<Category[]>([
  { name: 'Topwear', product: null as Product | null },
  { name: 'Bottomwear', product: null as Product | null },
  { name: 'Accessory', product: null as Product | null },
  { name: 'Footwear', product: null as Product | null },
]);

const categoryMapping = {
  'Topwear': ['shirt', 'outerwear'],
  'Bottomwear': ['pant'],
  'Accessory': ['accessory'],
  'Footwear': ['shoe'],
}
const selectedCategory = ref('')

const openEdit = ref(props.edit);
const outfit = ref(props.selectedOutfit?.products || []);
const outfitTags = ref(props.selectedOutfit.true_tags);


const selectTable = (name: string) => {
  selectedCategory.value = name;
  const subCategories = categoryMapping[name];

  filteredClothes.value = clothes.value.filter((product: Product) => 
    product.category && subCategories.includes(product.category.toLowerCase())
  );
}

const addProduct = (product: Product) => {
  const category = categories.value.find(cat => cat.name === selectedCategory.value);
  if (category && !category.product) {
    category.product = product;
    outfit.value.push(product);
    updateTags();
  }
}


const uploadOutfit = async () => {
  if (outfit.value.length !== 4) {
    ElNotification({
      title: 'Error',
      message: 'Please fill in all the items!',
      type: 'error',
    });
    return;
  }
  
  const outfitData: any = {
    outfit: {}
  };

  const outfitId = props.selectedOutfit?.outfit_id || null;
  if (outfitId) {
    outfitData.outfit.outfit_id = outfitId;
  }

  categories.value.forEach(category => {
    const product = category.product;

    if (product) {
      const productId = product.ProductID;
      const productCategory = product.category.toLowerCase();

      switch (productCategory) {
        case 'shirt':
        case 'outerwear':
          outfitData.outfit.shirt_id = productId;
          break;
        case 'pant':
          outfitData.outfit.pant_id = productId;
          break;
        case 'accessory':
          outfitData.outfit.accessory_id = productId;
          break;
        case 'shoe':
          outfitData.outfit.shoe_id = productId;
          break;
        case 'dress':
          outfitData.outfit.dress_id = productId;
          break;
        default:
          break;
      }
    }
  });

  try {
    const response = await $authApi.post('/save-outfit', outfitData);

    if (response.status === 200) {
      ElNotification({
        title: 'Success',
        message: `Outfit saved successfully!`,
        type: 'success',
      });
      openEdit.value = false;
      categories.value.forEach(category => category.product = null);
    }
  } catch (error) {
    console.error('Error uploading outfit:', error);
  }
}

const getData = async () => {
  try {
    const response = await $authApi.get('/user/products');

    clothes.value = response.data.products.map((product: any) => ({
      ProductID: product.ProductID,
      articleType: product.articleType,
      baseColour: product.baseColour,
      category: product.category,
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
    }))
    filteredClothes.value = clothes.value;
  } catch (error) {
    console.error('Error fetching products:', error);
  }
}


const removeProduct = (category: Category) => {
  if (category.product) {
    const productIndex = outfit.value.findIndex(
      (product: Product) => product.ProductID === category.product!.ProductID
    );

    if (productIndex !== -1) {
      outfit.value.splice(productIndex, 1);
    }
    category.product = null;
    updateTags();
  }
};

const updateOutfitCategories = () => {
  categories.value.forEach(category => category.product = null);

  if (outfit.value.length === 0) {
    return;
  }

  outfit.value.forEach((product: Product) => {
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

const handleClose = (done: () => void) => {
  if (outfit.value.length === 4) {
    done();
  } else {
    ElNotification({
    title: 'Error',
    message: 'Please fill in all the items!',
    type: 'error',
    })
  }
}

const emit = defineEmits<{ (event: 'close'): void }>();

const emitCloseEvent = () => {
  setTimeout(() => {
    emit('close');
  }, 300);
};

watch(input, (newInput) => {
  filteredClothes.value = clothes.value.filter((product: Product) => 
    product.productDisplayName.toLowerCase().includes(newInput.toLowerCase())
  );
});
</script>

<style>
.font {
  color: var(--third-color);
  letter-spacing: 1px;
  font-size: 7px;
  font-weight: 350; 
}
.product-images {
  display: flex;
  flex-direction: column;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.el-card {
  width: 100%;
}

.el-image {
  width: 100%;
  height: 150px;
}
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

.upload-mimic.selected {
  border-color: var(--primary-color);
}

.upload-mimic:hover {
  border-color: var(--primary-color);
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
