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
      <button @click="showDownloadModal" class="dl-button">
        <img src="@/assets/downloadIcon.svg" alt="" class="icon"/>
        Download results
      </button>
    </div>
  </header>
</template>


<style scoped>
.header {
  text-align: center;
  margin-bottom: 20px;
}
.dl-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
}
</style>