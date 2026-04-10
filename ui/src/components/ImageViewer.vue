<script setup>
defineProps({
  image: Object
})
</script>


<template>
  <div class="image-viewer">
    <transition name="slide" mode="out-in">
      <div :key="image.image_url"> <img
          :src="image.image_url" 
          class="main-image"
          loading="lazy" 
        />

        <div class="objects">
          <div v-for="(obj, i) in image.objects" :key="i" class="object-row">
            <img
              :src="obj.crop_url"
              class="crop"
              loading="lazy"
            />
            <div class="info">
              <strong>{{ obj.pred }}</strong>
              <div class="topk">
                <div v-for="(t,k) in obj.top_k" :key="k">
                  {{ t[0] }} - {{ t[1].toFixed(3) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>


<style>
.image-viewer {
  color: var(--ui-amber);
}
.main-image {
  max-width: 400px;
  display: block;
  margin-bottom: 10px;
}
.crop {
  width: 80px;
  height: 80px;
  object-fit: cover;
  margin-right: 10px;
  border: 1px solid #ccc;
}
.object-row {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}
.slide-enter-from {
  transform: translateX(50px);
  opacity: 0;
}
.slide-leave-to {
  transform: translateX(-50px);
  opacity: 0;
}
.topk {
  font-size: 12px;
  color: var(--ui-grey);
}
</style>