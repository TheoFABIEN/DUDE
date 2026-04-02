<script setup>
const emit = defineEmits(['files-uploaded'])

function onFileChange(event) {
  const file = event.target.files[0]
  if (file) {
    emit('files-uploaded', file)
  }
}
</script>


<template>
  <div class="upload-zone">
    <input type="file" @change="onFileChange" accept=".zip" />
    <p>Come on, drop your images zip file</p>
  </div>
</template>


<style>
.upload-zone {
  border: 2px dashed #ccc;
  padding: 40px;
  text-align: center;
  margin-bottom: 20px;
}
</style>