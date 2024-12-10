<template>
  <Header />

  <div v-if="isClient" class="tags">
    <el-tag 
      v-for="tag in dynamicTags" 
      :key="tag" 
      closable 
      :disable-transitions="false" 
      @close="handleClose(tag)"
      class="tag-color">
      {{ tag }}
    </el-tag>
    <el-select 
      size="small"
      placeholder="+ New Tag"
      style="width: 200px"
      @change="handleSelect"
    >
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      /> 
    </el-select>
  </div>

</template>


<script lang="ts" setup>
import { onMounted, ref } from 'vue'

const isClient = ref(false);

onMounted(() => {
  isClient.value = true;
});

const dynamicTags = ref<string[]>([])

const handleClose = (tag: string) => {
  dynamicTags.value.splice(dynamicTags.value.indexOf(tag), 1)
}
const handleSelect = (value: string) => {
  if (value && !dynamicTags.value.includes(value)) {
    dynamicTags.value.push(value)
  }
}

const options = ref([
  {
    value: 'Option1',
    label: 'Option1',
  },
  {
    value: 'Option2',
    label: 'Option2',
  },
  {
    value: 'Option3',
    label: 'Option3',
  },
  {
    value: 'Option4',
    label: 'Option4',
  },
  {
    value: 'Option5',
    label: 'Option5',
  },
])
</script>

<style>
.tags {
  padding-left: 20px;
  padding-right: 20px;
}

.tag-color {
  color: #838C8B;
  background-color: #ffffff;
  border-color: #838C8B;
}
</style>
