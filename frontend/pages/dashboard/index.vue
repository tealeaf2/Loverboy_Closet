<template>
  <el-container>
    <el-header>
      <el-container class="header-container">
        <el-main>
          <el-input v-model="nameSearchQuery" placeholder="Input name" prefix-icon="el-icon-search" clearable
            size="small" class="w-full" />
          <el-input v-model="descriptionSearchQuery" placeholder="Input description" prefix-icon="el-icon-search"
            clearable size="small" class="w-full" />
        </el-main>
        <el-aside class="aside-center">

          <el-button type="success" v-if="searchPerformed == false" @click="performSearch()">
            Search
          </el-button>
          <el-button type="danger" v-if="searchPerformed == true" @click="performSearch()">
            Back
          </el-button>
          <el-button type="primary" @click="handleAdd()" v-if="searchPerformed == false">
            Add
          </el-button>

        </el-aside>
      </el-container>

    </el-header>
      <el-pagination :current-page="currentPage" :page-size="pageSize" :total="filteredClothInfo.length"
      @current-change="handlePageChange" layout="total, prev, pager, next, jumper"></el-pagination>
    <el-container>
      <el-main class="table">
        <el-table :data="paginatedClothInfo" border width="800">
          <template #empty>
            <div class="flex flex-row justify-center items-center space-x-2">
              <span>click + to add new clothes</span>
            </div>
          </template>
          <el-table-column prop="ID" label="ID" align="center">
            <template #default="{ row, $index }">
              <!-- <el-input v-if="$index === editingIndex" v-model="row.ID" placeholder="ID?" size="small">
              </el-input> -->
              <span>{{ row.ID }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="name" min-width="60px" align="center">
            <template #default="{ row, $index }">
              <el-input v-if="$index === editingIndex" v-model="row.name" placeholder="name?" size="small">
              </el-input>
              <span v-else>{{ row.name }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="sex" label="sex" min-width="60px" align="center">
            <template #default="{ row, $index }">
              <el-select v-if="$index === editingIndex" v-model="row.sex" filterable clearable placeholder="sex?"
                size="small" style="width: 100%">
                <el-option v-for="item in sexOptions" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
              <span v-else>{{ getSexLabel(row.sex) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="brand" label="brand" min-width="60px" align="center">
            <template #default="{ row, $index }">
              <el-input v-if="$index === editingIndex" v-model="row.brand" placeholder="brand?" size="small">
              </el-input>
              <span v-else>{{ row.brand }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="description" min-width="60px" align="center">
            <template #default="{ row, $index }">
              <el-input v-if="$index === editingIndex" v-model="row.description" placeholder="description?"
                size="small">
              </el-input>
              <span v-else>{{ row.description }}</span>
            </template>
          </el-table-column>
          <el-table-column label="operation" align="center" min-width="100px" v-if="searchPerformed == false">
            <template #default="{ row, $index }">
              <div class="flex flex-row justify-center items-center">
                <template v-if="$index === editingIndex">
                  <el-button type="success" size="small" plain @click="handleSave(row, $index)">Save</el-button>
                  <el-button type="info" size="small" plain @click="handleCancel(row, $index)">Cancel</el-button>
                </template>
                <template v-else>
                  <el-button type="primary" size="small" plain @click="handleEdit(row, $index)">
                    Edit
                  </el-button>
                  <el-popconfirm title="Are your sure?" @confirm="handleDelete(row, $index)" style="margin-left: 10px">
                    <template #reference>
                      <el-button type="danger" size="small" plain>Delete</el-button>
                    </template>
                  </el-popconfirm>
                </template>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </el-container>

</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { onMounted, nextTick } from 'vue'

const { $api } = useNuxtApp()

interface clothInfo {
  ID: string
  name: string
  brand: string
  sex: string
  description: string
}

const sexOptions = [
  { value: 1, label: 'Male' },
  { value: 2, label: 'Female' }
]

/* ---------------------------------- Table Data ---------------------------------- */


const clothInfo = ref<clothInfo[]>([])

const clothInfoRef = ref<FormInstance>()

const nameSearchQuery = ref('')  // Search query for name
const descriptionSearchQuery = ref('')  // Search query for description

const searchPerformed = ref(false) // Track if search is performed
const currentPage = ref(1)
const pageSize = ref(40)

const paginatedClothInfo = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredClothInfo.value.slice(start, end)
})

const handlePageChange = (page: number) => {
  currentPage.value = page
}


/* ------------------------------ Editing Index ------------------------------ */
const editingIndex = ref<number>(-1)

/* ------------------------------- Row Data Before Editing ------------------------------- */
const beforeEditRow = ref<clothInfo>({
  ID: '',
  name: '',
  brand: '',
  sex: '',
  description: ''
})

/* --------------------------------- Empty Data When Added -------------------------------- */
const addContractRow: clothInfo = {
  ID: '',
  name: '',
  brand: '',
  sex: '',
  description: ''
}


/* ---------------------------------- Computed Property for Filtered Data ---------------------------------- */
onMounted(() => {
  getData();
})

const getData = async () => {
  try {
    const response = await $api.get('/products');
    console.log(response.data);

    clothInfo.value = response.data.map((product: any) => ({
      ID: product.ProductID,
      name: product.ProductName,
      brand: product.ProductBrand,
      sex: product.Gender === 'Men' ? 1 : 2,
      description: product.Description
    }))

  } catch (error) {
    console.error('Error fetching products:', error);
  }
}

const filteredClothInfo = computed(() => {
  // Check if a search was performed and filter based on name and description
  if (!searchPerformed.value || (!nameSearchQuery.value && !descriptionSearchQuery.value)) {
    return clothInfo.value
  }
  return clothInfo.value.filter((row) =>
    (!nameSearchQuery.value || row.name.includes(nameSearchQuery.value)) &&
    (!descriptionSearchQuery.value || row.description.includes(descriptionSearchQuery.value))
  )
})

/* ---------------------------------- Perform Search Operation ---------------------------------- */
const performSearch = () => {
  searchPerformed.value = !searchPerformed.value
}


/* ---------------------------------- Reset Table --------------------------------- */
const resetTable = () => {
  editingIndex.value = -1
  beforeEditRow.value = { ...addContractRow }
}


/* ---------------------------------- Table Operation ---------------------------------- */
const handleAdd = async () => {
  if (editingIndex.value > -1) {
    ElMessage.warning('Please complete the row being edited first')
    return
  }
  const actualIndex = clothInfo.value.length;
  const entry = { ...addContractRow};
  editingIndex.value = actualIndex % pageSize.value;

  currentPage.value = Math.ceil(actualIndex / pageSize.value);

  const payload = {
    "ProductName": entry.name,
    "ProductBrand": entry.brand,
    "Gender": '',
    "Price": 0,
    "NumImages": 0,
    "Description": '',
    "PrimaryColor": ''
  }

  try {
    const response = await $api.post(`/products`, payload)
    clothInfo.value.push({
      ID: response.data.ProductID,
      name: entry.name,
      brand: entry.brand,
      sex: entry.sex || '',
      description: entry.description || ''
    });

  } catch(error) {
    console.error(error);
  }
}

const handleEdit = (row: clothInfo, index: number) => {
  if (editingIndex.value > -1) {
    ElMessage.warning('Please complete the row being edited first')
    return
  }
  beforeEditRow.value = { ...row }
  editingIndex.value = index
}

const handleSave = async (row: clothInfo, index: number) => {
  if (!row.name || !row.brand || !row.sex) {
    ElMessage.warning('Please fill in all required fields')
    return
  }
  const actualIndex = (currentPage.value - 1) * pageSize.value + index;
  clothInfo.value[actualIndex] = { ...row }
  resetTable()

  const payload = {
    "ProductName": row.name,
    "ProductBrand": row.brand,
    "Gender": row.sex === 1 ? "Male" : "Woman",
    "Description": row.description
  }

  try {
    const response = await $api.put(`/products/${row.ID}`, payload);
  } catch(error) {
    console.error(error);
  }
}

const handleDelete = (row: clothInfo, index: number) => {
  const actualIndex = (currentPage.value - 1) * pageSize.value + index;

  const rowId = row.ID;
  try {
    const response = $api.delete(`/products/${rowId}`);
    clothInfo.value.splice(actualIndex, 1);

  } catch (error) {
    console.error('Error deleting item:', error);
  }
}

const handleCancel = (row: clothInfo, index: number) => {
  const actualIndex = (currentPage.value - 1) * pageSize.value + index; 

  if (Object.values(beforeEditRow.value).some((value) => value !== '')) {
    clothInfo.value[actualIndex] = { ...beforeEditRow.value }
  } else {
    clothInfo.value.splice(actualIndex, 1)
  }
  resetTable()
}

const getSexLabel = (value: number) => {
  return sexOptions.find((option) => option.value === value)?.label || ''
}
</script>

<style>
.table {
  width: 90%;
}

.addButton {
  width: 10%;
}

.aside-center {
  display: flex;
  justify-content: center;
  /* Centers buttons horizontally */
  align-items: center;
  /* Centers buttons vertically */
  height: 100%;
  /* Ensure it takes up the full height of el-aside */
}

.header-container {
  display: flex;
  justify-content: center;
  /* Centers buttons horizontally */
  align-items: center;
  /* Centers buttons vertically */
  height: 100%;
  /* Ensure it takes up the full height of el-aside */
}
</style>