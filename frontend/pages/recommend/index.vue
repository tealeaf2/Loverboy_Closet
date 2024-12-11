<template>
  <Header />

  <div>
    select specific clothing
  </div>

  <div v-if="isClient" class="tags">
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

    <el-tag 
      v-for="tag in dynamicTags" 
      :key="tag" 
      closable 
      :disable-transitions="false" 
      @close="handleClose(tag)"
      class="tag-color">
      {{ tag }}
    </el-tag>
  </div>


  <div>
    based on your clothes
  </div>

</template>


<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import options from './options'

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
