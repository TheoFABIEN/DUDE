<script setup>

const emit = defineEmits([
  'openDownloadModal'
])
const props = defineProps({
  results: Object
})

function showDownloadModal() {
  emit('openDownloadModal')
}

</script>


<template>
  <header class="header">
    <h1>D.U.D.E.</h1>
    <div v-if="props.results?.status === 'done'" class="actions">
      <button @click="showDownloadModal">Download results</button>
    </div>
  </header>
</template>


<style scoped>
.header {
  text-align: center;
  margin-bottom: 20px;
}
</style>