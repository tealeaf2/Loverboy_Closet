<template>
  <Header></Header>
  <ClosetSidebar v-model="selectedTab"></ClosetSidebar>
  <div class="shell">
    <input type="checkbox" id="checkbox">
    <label for="checkbox"></label>
    <input type="text" placeholder="search" class="input" id="input" v-model="searchQuery">
    <div @click="dialogFormVisible = true" class="add"></div>
  </div>
  <div class="container">
    <div v-for="item in filteredClothes" :key="item.ProductID" class="box">
      <div class="top-bar"></div>
      <div class="pic">
        <img :src="item.image_url" alt="">
      </div>
      <div class="star-icon" @click="toggleFavorite(item)">
        <el-icon v-if="!item.favorite"><Star /></el-icon>
        <el-icon v-else class="selected"><StarFilled/></el-icon>
      </div>
      <div class="info">
        <strong>{{ item.productDisplayName }}</strong>
        <div class="buttons">

          <a href="#" @click.prevent="deleteItem(item.ProductID)"><i class="fi fi-rs-trash"></i>Delete</a>
          <a href="#" @click.prevent="toggleForm(item)"><i class="fi fi-rs-eye"></i>View</a>
        </div>
      </div>
    </div>
    <ClosetDrawer :drawer="isFormVisible" :selectedItem="selectedItem" v-if="isFormVisible" @close="closeForm" />

    <div v-if="isClient">
      <el-dialog v-model="dialogFormVisible" title="" width="1000">
        <el-form>
          <el-input
          v-model="input"
          style="width: 80%"
          placeholder="Search Clothes"
          :prefix-icon="Search"
        />
        <div class="demo-pagination-block">
          <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :size="size" :disabled="disabled"
            :background="background" layout="total, prev, pager, next, jumper" :total="filterTableData.length"/>
        </div>

        <el-skeleton v-if="loading" :rows="2" animated />
        <el-table v-if="!loading" 
          :data="paginatedClothes" 
          style="width: 100%" 
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column label="ProductID" property="ProductID" width="120px"/>
          <el-table-column label="Name" property="productDisplayName" width="500px"/>
          <el-table-column label="Category" property="masterCategory" width="150px"/>
          <el-table-column label="Image" width="100px">
            <template #default="scope">
              <el-image style="width: 50%; height: 50%" :src="scope.row.image_url" />
            </template>
          </el-table-column>
        </el-table>

        </el-form>
        <template #footer>
          <div class="dialog-footer">
            <el-button class="cancel-button" @click="clearSelection">Cancel</el-button>
            <el-button class="confirm-button" primary @click="addProducts">
              Add
            </el-button>
          </div>
        </template>
      </el-dialog>
    </div>

  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue';
import { useNuxtApp, useRuntimeConfig } from '#app';
const selectedTab = ref<string>('');
const { $api, $authApi } = useNuxtApp()
const searchQuery = ref('');
import { ComponentSize, ElNotification, ElLoading } from 'element-plus'
import { Search, Star, StarFilled } from '@element-plus/icons-vue'

const config = useRuntimeConfig();

definePageMeta({
  middleware: [
    'auth'
  ]
});

onMounted(() => {
  getData();
  getAllClothes();
  isClient.value = true;
})

const allClothes = ref<Product[]>([]);
const isFormVisible = ref(false);
const isClient = ref(false);
const dialogFormVisible = ref(false)
const selectedItem = ref<Product | null>(null);
const currentPage = ref(1)
const pageSize = ref(15);
const size = ref<ComponentSize>('default')
const background = ref(false)
const disabled = ref(false)
const input = ref('')
const loading = ref(true)

const toggleFavorite = (item: Product) => {
  item.favorite = !item.favorite;
  updateFavorite(item);
};

const updateFavorite = async (item: Product) => {
  try {
    const response = await $authApi.put(`/toggle-favorite/products/${item.ProductID}`);
    if (response.status === 200) {
      console.log('Favorite toggled successfully:', response.data);
    } 
  } 
  catch (error) {
    console.error('Error updating:', error);
  }
};

const toggleForm = (item: Product) => {
  selectedItem.value = item;
  isFormVisible.value = !isFormVisible.value;
};

const closeForm = () => {
  isFormVisible.value = false;
  selectedItem.value = null;
};

interface Product {
  ProductID: number;
  articleType: string;
  baseColour: string;
  favorite: boolean;
  category: string;
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

const clothes = ref<Product[]>([]);
const categoryMapping = {
  '0': 'Favorite',
  '1': 'All',
  '2': 'shirt',
  '3': 'pant',
  '4': 'accessory',
  '5': 'shoe',
  '6': 'outerwear',
  '7': 'dress',
};

const filterTableData = computed(() =>
  allClothes.value.filter(
    (data) =>
      !input.value ||
      data.productDisplayName.toLowerCase().includes(input.value.toLowerCase())
  )
)

const paginatedClothes = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filterTableData.value.slice(start, end);
});

const selectedItems = ref<Product[]>([]);
const handleSelectionChange = (selection: Product[]) => {
  selectedItems.value = selection;
  console.log('Selected Items:', selectedItems.value);
};

const clearSelection = () => {
  dialogFormVisible.value = false;
  selectedItems.value = [];
}

const addProducts = async () => {
  dialogFormVisible.value = false;
  const payload = selectedItems.value;
  
  try {
    const response = await $authApi.post('/products', {
      products: payload.map((product: Product) => ({
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
      })),
    })
    clothes.value = [...clothes.value, ...selectedItems.value];
    console.log('Products added successfully:', response.data);

    ElNotification ({
      title: 'Success',
      message: 'Items added successfully',
      type: 'success',
    })

    selectedItems.value = [];
  } catch(error) {
    console.error('Error adding products:', error);
  }
}

const getAllClothes = async () => {
  try {
    const response = await $api.get('/products');

    allClothes.value = response.data.products.map((product: any) => ({
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
    }))
    loading.value = false;
    console.log(allClothes);
  } catch (error) {
    console.error('Error fetching products:', error);
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
  } catch (error) {
    console.error('Error fetching products:', error);
  }
}

const filteredClothes = computed(() => {
  if (!selectedTab.value || selectedTab.value === '1') {
    return clothes.value.filter(product =>
      product.productDisplayName.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  }
  else if (selectedTab.value == '0'){
    return clothes.value.filter(product =>
      product.favorite &&
      product.productDisplayName.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  }

  return clothes.value
    .filter(product => categoryMapping[selectedTab.value] === product.category)
    .filter(product =>
      product.productDisplayName.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
})

const deleteItem = async (productID: number) => {
  const user = 20;
  try {
    const response = await $authApi.delete(`/user/products/${productID}`);
    if (response.status === 200) {
      console.log(`Product ${productID} successfully removed from user ${user}`);
      clothes.value = clothes.value.filter(product => product.ProductID !== productID);

    } else {
      console.error('Failed to delete the product:', response.data);
    }
  } catch (error) {
    console.error('Error fetching products:', error);
  }
};

</script>

<style scoped>
@import url('https://cdn-uicons.flaticon.com/2.6.0/uicons-regular-rounded/css/uicons-regular-rounded.css');
@import url('https://cdn-uicons.flaticon.com/2.6.0/uicons-regular-straight/css/uicons-regular-straight.css');
@import url('https://cdn-uicons.flaticon.com/2.6.0/uicons-regular-straight/css/uicons-regular-straight.css');

* {
  box-sizing: border-box;
}

.selected {
  color: var(--primary-color)
}

.star-icon {
  position: absolute;
  top: 10px; 
  right: 10px;
  z-index: 1;
}

.shell {
  position: relative;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 120px;
  gap: 10px;
}

.input {
  padding: 0;
  width: 0;
  height: 0;
  background: none;
  border: none;
  border-radius: 20px;
  outline: none;
  transition: .5s;
}

#checkbox {
  visibility: hidden;
}

[for=checkbox] {
  display: block;
  width: 70px;
  height: 70px;
  border-radius: 20px;
  background-color: var(--primary-color);
  /* Desired color */
  mask: url(/picture/search.png) no-repeat center;
  mask-size: contain;
  -webkit-mask: url(/picture/search.png) no-repeat center;
  -webkit-mask-size: contain;
}

#checkbox:checked~label {
  border-radius: 10px;
  background-color: var(--primary-color);
  /* Desired color */
  mask: url(/picture/cross.png) no-repeat center;
  mask-size: contain;
  -webkit-mask: url(/picture/cross.png) no-repeat center;
  -webkit-mask-size: contain;
  margin: 0 -5px;
}

#checkbox:checked~input {
  width: 400px;
  border-radius: 10px;
  color: black;
  visibility: visible;
  padding: 10px;
  height: 80px;
  background: none;
  border: 4px solid var(--primary-color);
  transition: .5s;
  font-size: 24px;
}

.add {
  display: block;
  width: 50px;
  height: 50px;
  background-color: var(--primary-color);
  /* Desired color */
  mask: url(/picture/plus.png) no-repeat center;
  mask-size: contain;
  -webkit-mask: url(/picture/plus.png) no-repeat center;
  -webkit-mask-size: contain;
}

.box {
  width: 266px;
  height: 420px;
  background-color: var(--secondary-color);
  box-shadow: 2px 2px 30px rgba(0, 0, 0, .05);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 30px 20px 30px 20px;
  border-radius: 10px;
  margin: 20px;
  position: relative;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.top-bar {
  width: 50%;
  height: 4px;
  position: absolute;
  left: 50%;
  top: 0;
  transform: translateX(-50%);
  background-color: var(--primary-color);
}

.nav {
  display: flex;
  flex-direction: row-reverse;
  width: 100%;
}

.fi-rr-shirt-long-sleeve {
  font-size: 18px;
  color: black;
  z-index: 1;
}

.fi-rr-shirt-long-sleeve.wearing {
  color: red;
}

.pic img {
  width: 266px;
  height: 266px;
  position: absolute;
  left: 0;
  top: 10px;

}

.info {
  display: flex;
  flex-direction: column;
  align-items: center;

}

strong {
  font-size: 16px;
  text-align: center;
  padding-bottom: 14px;
  line-height: 18px;
}

.buttons {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 80%;
}

.buttons a {
  text-decoration: none;
  font-size: 18px;
  text-align: center;
  color: var(--primary-color);
  user-select: none;
  cursor: pointer;
}

.fi-rs-eye {
  font-size: 14px;
  margin-right: 2px;
}

.fi-rs-trash {
  font-size: 14px;
  margin-right: 2px;
}

.detail-box {
  position: absolute;
  left: 100%;
  top: 0;
  width: 390px;
  height: 390px;
  z-index: 1;
  transition: opacity 1s ease-in-out;
}

.details {
  position: relative;
  width: 100%;
  height: 100%;
  background-color: var(--primary-color);
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.type {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.type strong {
  font-size: 30px;
  line-height: 1px;
}

.cancel-button {
  border: 1px solid #c07858;
  color: #c07858;
}

.confirm-button {
  background-color: #c07858;
  color: white;
}

.demo-pagination-block {
  margin-top: 10px;
  margin-bottom: 10px;
  color: var(--third-color);
}
</style>