<script setup>
defineProps({
  images: Array
})
</script>

<template>
  <div class="image-viewer">
    <div v-for="(img, index) in images" :key="index" class="image-block">

      <img
        :src="'data:image/jpeg;base64,' + img.image"
        class="main-image"
      />

      <div class="objects">
        <div
          v-for="(obj, i) in img.objects"
          :key="i"
          class="object-row"
        >
          <img
            :src="'data:image/jpeg;base64,' + obj.crop"
            class="crop"
          />

          <div class="info">
            <strong>{{ obj.pred }}</strong>

            <div class="topk">
              <div v-for="(t, k) in obj.top_k" :key="k">
                {{ t[0] }} — {{ t[1].toFixed(3) }}
              </div>
            </div>

          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<style>
.image-viewer {
  color: var(--ui-amber);
}
.image-block {
  margin-bottom: 30px;
}

.main-image {
  max-width: 400px;
  display: block;
  margin-bottom: 10px;
}

.object-row {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.crop {
  width: 80px;
  height: 80px;
  object-fit: cover;
  margin-right: 10px;
  border: 1px solid #ccc;
}

.info {
  font-size: 14px;
}

.topk {
  font-size: 12px;
  color: var(--ui-grey);
}
</style>