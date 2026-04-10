<script setup>
import { downloadResults } from '@/services/api'

const props = defineProps({
  results: Object
})

async function download() {
  const blob = await downloadResults(props.results)
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'results.zip'
  a.click()
  window.URL.revokeObjectURL(url)
}
</script>


<template>
  <header class="header">
    <h1>D.U.D.E.</h1>
    <div v-if="props.results?.status === 'done'" class="actions">
      <button @click="download">Download results</button>
    </div>
  </header>
</template>


<style scoped>
.header {
  text-align: center;
  margin-bottom: 20px;
}
button {
  color: var(--ui-pearl);
  background-color: var(--ui-grey);
  border: none;
}
button:hover {
  background-color: var(--ui-amber);
}
</style>