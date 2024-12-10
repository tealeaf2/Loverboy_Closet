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
        <el-form :model="form">
          Stuff
        </el-form>
        <template #footer>
          <div class="dialog-footer">
            <el-button class="cancel-button" @click="dialogFormVisible = false">Cancel</el-button>
            <el-button class="confirm-button" primary @click="dialogFormVisible = false">
              Confirm
            </el-button>
          </div>
        </template>
      </el-dialog>
    </div>

  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, reactive } from 'vue';
import { useNuxtApp } from '#app';
const selectedTab = ref<string>('');
const { $api } = useNuxtApp()
const searchQuery = ref('');

onMounted(() => {
  getData();
  isClient.value = true;
})

const form = reactive({
  name: '',
  region: '',
  date1: '',
  date2: '',
  delivery: false,
  type: [],
  resource: '',
  desc: '',
})

const isFormVisible = ref(false);
const isClient = ref(false);
const dialogFormVisible = ref(false)
const selectedItem = ref<Product | null>(null);

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
  '0': 'All',
  '1': 'Apparel',
  '2': 'Footwear',
  '3': 'Accessories'
};

const getData = async () => {
  try {
    const response = await $api.get('/user/20/products');

    clothes.value = response.data.products.map((product: any) => ({
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
  } catch (error) {
    console.error('Error fetching products:', error);
  }
}

const filteredClothes = computed(() => {
  if (!selectedTab.value || selectedTab.value === '0') {
    return clothes.value.filter(product =>
      product.productDisplayName.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  }

  return clothes.value
    .filter(product => categoryMapping[selectedTab.value] === product.masterCategory)
    .filter(product =>
      product.productDisplayName.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
})

const deleteItem = async (productID: number) => {
  const user = 20;
  try {
    const response = await $api.delete(`/user/${user}/products/${productID}`);
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
</style>