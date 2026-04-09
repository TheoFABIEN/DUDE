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

    <div class="loader" v-else-if="results.status === 'uploading'">
    </div>

    <div v-else-if="results.status === 'done'">
      <ImageViewer :images="results.pred_output" />
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