<script setup>
import { ref, watch } from 'vue'
import ImageViewer from './ImageViewer.vue'
import DeleteModal from './deleteModal.vue'

const props = defineProps({
  results: Object
})

const currentIndex = ref(0)

watch(() => props.results, () => {
  currentIndex.value = 0
})

function prev() {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}
function next() {
  if (currentIndex.value < props.results.pred_output.length - 1) {
    currentIndex.value++
  }
}

const showDeleteModal = ref(false)
const deleteTarget = ref(null)

function requestDelete(imgIndex, objIndex) {
  deleteTarget.value = { imgIndex, objIndex }
  showDeleteModal.value = true
}
function cancelDelete() {
  showDeleteModal.value = false
  deleteTarget.value = null
}
function confirmDelete() {
  const { imgIndex, objIndex } = deleteTarget.value
  props.results.pred_output[imgIndex].objects.splice(objIndex, 1)
  showDeleteModal.value = false
  deleteTarget.value = null
}
</script>


<template>
  <div class="results-panel">
    <div class="header">
      <h2>Results</h2>

      <div v-if="results?.status === 'done'" class="nav-buttons">
        <button @click="prev">&lt;</button>
        <span>{{ currentIndex + 1 }} / {{ results.pred_output.length }}</span>
        <button @click="next">&gt;</button>
      </div>
    </div>

    <div v-if="!results">
      Nothing to show
    </div>

    <div class="loader" v-else-if="results.status === 'uploading'">
    </div>

    <div v-else-if="results.status === 'done'">
      <ImageViewer 
        :image="results.pred_output[currentIndex]" 
        :img-index="currentIndex"
        @request-delete="requestDelete"
      />
    </div>

    <DeleteModal 
      v-if="showDeleteModal"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />

    <div v-else-if="results.status === 'novalidinput'">
      No valid images found.
    </div>
  </div>
</template>

<style>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.nav-buttons {
  display: flex;
  gap: 10px;
  align-items: center;
  button {
    color: var(--ui-pearl);
    font-weight: bold;
    background-color: var(--ui-darkblue); 
    border: none;
  }
}
button {
  padding: 5px 10px;
  cursor: pointer;
}
.loader {
  width: fit-content;
  margin: 0 auto;
  font-weight: bold;
  font-family: sans-serif;
  padding-bottom: 8px;
  background: linear-gradient(currentColor 0 0) 0 100%/0% 3px no-repeat;
  animation: l2 2s linear infinite;
}
.loader:before {
  content:"Loading..."
}
@keyframes l2 {to{background-size: 100% 3px}}
</style>