<template>
  <div class="image-viewer">
    <div v-for="img in images" :key="img.filename" class="image-card">
      <canvas :ref="el => drawImage(el, img)"></canvas>
      <p>{{ img.filename }}</p>
    </div>
  </div>
</template>

<script setup>
import {onMounted} from 'vue'
defineProps({
    images: Array
})

function drawImage(canvas, imgData) {
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    const image = new Image()
    image.onload = () => {
        canvas.width = image.width
        canvas.height = image.height
        ctx.drawImage(image, 0, 0)

        imgData.boxes.forEach(box => {
            const [x1, y1, x2, y2] = box
            const w = x2 - x1
            const h = y2 - y1

            ctx.strokeStyle = 'red'
            ctx.lineWidth = 20
            ctx.strokeRect(x1, y1, w, h)
            ctx.fillStyle = 'red'
        });
    }
    image.src = `data:image/jpeg;base64,${imgData.image}`
}
</script>

<style>
.image-viewer {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}
.image-card {
  border: 1px solid #ddd;
  padding: 10px;
}
canvas {
  width: 100%;
}
</style>