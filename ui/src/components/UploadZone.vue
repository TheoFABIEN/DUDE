<script setup>
import { ref } from 'vue'

const emit = defineEmits(['files-uploaded'])

const active = ref(false)

const setActive = () => { active.value = true }
const setInactive = () => { active.value = false }

function onDrop(event) {
  setInactive()
  const file = event.dataTransfer.files[0]
  if (file) {
    emit('files-uploaded', file)
  }
}

function onFileChange(event) {
  const file = event.target.files[0]
  if (file) {
    emit('files-uploaded', file)
  }
}
</script>


<template>
  <div 
    @dragenter.prevent="setActive" 
    @dragleave.prevent="setInactive" 
    @dragover.prevent
    @drop.prevent="onDrop"
    :class="{ 'active-dropzone': active }"
    class="upload-zone"
  >
    <span>Drop your zip file here</span>
    <span>OR</span>
    <label for="dropzoneFile">Select File</label>
    <input type="file" id="dropzoneFile" @change="onFileChange" accept=".zip" />
  </div>
</template>


<style scoped>
.upload-zone {
  border: 2px dashed var(--ui-grey);
  background-color: var(--ui-anthracite);
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  row-gap: 16px;
  transition: 0.3s ease all;
  backdrop-filter: blur(10px);
}
.active-dropzone {
  color: #fff;
  border-color: #fff;
  background-color: var(--ui-anthracite);
}
.upload-zone label {
  padding: 8px 12px;
  transition: 0.3s ease all;
  cursor: pointer;
}
.upload-zone input {
  display: none;
}
</style>