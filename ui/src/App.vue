<script setup>
import { ref } from 'vue'
import { uploadZip } from './services/api'
import HeaderBar from '@/components/HeaderBar.vue'
import UploadZone from '@/components/UploadZone.vue'
import ResultsPanel from '@/components/ResultsPanel.vue'
import DownloadModal from '@/components/DownloadModal.vue'
import SettingsModal from '@/components/SettingsModal.vue'

const results = ref(null)
const isDownloadModalOpen = ref(false)
const isSettingsModalOpen = ref(false)

async function handleUpload(file) {
  results.value = { status: 'uploading' }
  const response = await uploadZip(file)
  results.value = response
}

function openDownloadModal() {isDownloadModalOpen.value = true}
function closeDownloadModal() {isDownloadModalOpen.value = false}

function openSettingsModal() {isSettingsModalOpen.value = true}
function closeSettingsModal() {isSettingsModalOpen.value = false}
</script>


<template>
  <div class="app-container">
    <HeaderBar :results="results" @openDownloadModal="openDownloadModal"/>
    <UploadZone @files-uploaded="handleUpload" />
    <ResultsPanel :results="results" @openSettingsModal="openSettingsModal"/>
    <DownloadModal 
      v-if="isDownloadModalOpen" 
      :results="results"
      @close="closeDownloadModal">
    </DownloadModal>
    <SettingsModal
      v-if="isSettingsModalOpen"
      @close="closeSettingsModal">
    </SettingsModal>
  </div>
</template>


<style scoped>
.app-container {
  padding: 20px;
  max-width: 1000px;
  margin: auto;
}
</style>
