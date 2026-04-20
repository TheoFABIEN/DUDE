<script setup>
import { downloadResults } from '@/services/api'
import { ref } from 'vue'

const dlFormat = ref("default")

const props = defineProps({
  results: Object
})

const emits = defineEmits([
    "close"
])

function close() {
    emits("close")
}

async function download() {
  const blob = await downloadResults(props.results, dlFormat.value)
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = dlFormat.value === "coco"
    ? "coco_annotations.zip"
    : "results.zip"
  a.click()
  window.URL.revokeObjectURL(url)
  close()
}

</script>


<template>
    <div class="overlay" @click.self="close">
        <div class="modal">
            <h3>Choose download format</h3>
            <select v-model="dlFormat">
                <option value="default">Default</option>
                <option value="coco">COCO 1.0</option>
            </select>
            <div class="modal-buttons">
                <button id="download-btn" @click="download">Download</button>
                <button id="close-btn" @click="close">Cancel</button>
            </div>
        </div>
    </div>
</template>


<style scoped>

.overlay {
position: fixed;
inset: 0;
background: rgba(0,0,0,0.6);
display: flex;
justify-content: center;
align-items: center;
z-index: 2000;
}
.modal {
    display: flex;
    flex-direction: column;
    width: 350px;
    height: 200px;
    max-width: 90%;
    max-height: 90%;
    justify-content: center;
    align-items: center;
    z-index: 2000;
    background-color: var(--ui-anthracite);
    border-radius: 12px;
    select {
        width: 100%;
        padding: 6px;
        font-size: 14px;
    }
}
select {
    max-width: 90%;
}
.modal-buttons {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
    gap: 30px;
}

</style>