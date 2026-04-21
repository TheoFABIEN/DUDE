<script setup>
import { ref } from 'vue'
import { uploadZip } from './services/api'
import HeaderBar from '@/components/HeaderBar.vue'
import UploadZone from '@/components/UploadZone.vue'
import ResultsPanel from '@/components/ResultsPanel.vue'
import DownloadModal from '@/components/DownloadModal.vue'

const results = ref(null)
const isModalOpen = ref(false)

async function handleUpload(file) {
  results.value = { status: 'uploading' }
  const response = await uploadZip(file)
  results.value = response
}

function openDownloadModal() {isModalOpen.value = true}
function closeDownloadModal() {isModalOpen.value = false}
</script>


<template>
  <div class="app-container">
    <HeaderBar :results="results" @openDownloadModal="openDownloadModal"/>
    <UploadZone @files-uploaded="handleUpload" />
    <ResultsPanel :results="results" />
    <DownloadModal 
      v-if="isModalOpen" 
      :results="results"
      @close="closeDownloadModal">
    </DownloadModal>
  </div>
</template>


<style scoped>
.app-container {
  padding: 20px;
  max-width: 1000px;
  margin: auto;
}
</style>
