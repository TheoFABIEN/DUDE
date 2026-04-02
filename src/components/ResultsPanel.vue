<script setup>
import ImageViewer from './ImageViewer.vue';
defineProps({
  results: Object
})
</script>


<template>
  <div class="results-panel">
    <h2>Results</h2>

    <div v-if="!results">
      Nothing to show
    </div>

    <div v-else-if="results.status === 'uploading'">
      Uploading...
    </div>

    <div v-else-if="results.status === 'done'">
      <ImageViewer :images="results.images_output" />
    </div>
    <div v-else-if="results.status === 'novalidinput'">
      No valid images found in the provided zip file.
    </div>
  </div>
</template>


<style>
.results-panel {
  border-top: 1px solid #ddd;
  padding-top: 20px;
}
</style>