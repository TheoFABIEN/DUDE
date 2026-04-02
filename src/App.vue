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
    <HeaderBar />
    <UploadZone @files-uploaded="handleUpload" />
    <ResultsPanel :results="results" />
  </div>
</template>


<style>
.app-container {
  font-family: Arial, sans-serif;
  padding: 20px;
  max-width: 900px;
  margin: auto;
}
</style>
