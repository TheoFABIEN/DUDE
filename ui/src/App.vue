<script setup>
import { ref } from 'vue'
import HeaderBar from '@/components/HeaderBar.vue'
import UploadZone from '@/components/UploadZone.vue'
import ResultsPanel from '@/components/ResultsPanel.vue'

const results = ref(null)

import { uploadZip } from './services/api'

async function handleUpload(file) {
  results.value = { status: 'uploading' }
  const response = await uploadZip(file)
  results.value = response
}
</script>


<template>
  <div class="app-container">
    <HeaderBar :results="results" />
    <UploadZone @files-uploaded="handleUpload" />
    <ResultsPanel :results="results" />
  </div>
</template>


<style scoped>
.app-container {
  padding: 20px;
  max-width: 900px;
  margin: auto;
}
</style>
