<script setup>
defineProps({
  image: Object
})

function selectClass(obj, index) {
  if (!obj.original_top_k) {
    obj.original_top_k = [...obj.top_k]
  }
  if (index === 0) return
  const selected = obj.top_k[index]
  const newTopK = obj.top_k.filter((_, i) => i !== index)
  obj.top_k = [selected, ...newTopK]
  obj.pred = selected[0]
  obj.edited = true
}

function resetClass(obj) {
  if (obj.original_top_k) {
    obj.top_k = [...obj.original_top_k]
    obj.pred = obj.top_k[0][0]
    obj.edited = false
  }
}

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
            <div class="left">
              <img
                :src="obj.crop_url"
                class="crop"
                loading="lazy"
              />
              <div class="info">
                <strong>{{ obj.pred }}</strong>
                <div class="topk">
                  <div v-for="(t,k) in obj.top_k" 
                    :key="k"
                    class="topk-item"
                    @click="selectClass(obj, k)"
                  >
                    {{ t[0] }} - {{ t[1].toFixed(3) }}
                  </div>
                </div>
              </div>
            </div>
            <button v-if="obj.edited" @click="resetClass(obj)">Reset</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>


<style scoped>
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
.left {
  display: flex;
  align-items: center;
  gap: 10px;
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
.topk-item {
  cursor: pointer;
  &:hover {
    color: var(--ui-amber);
  }
  &:first-child {
    font-weight: bold;
  }
}
button {
  background: none;
  margin-left: auto;
  &:hover {
    background: none;
    color: var(--ui-amber);
  }
}

@media (max-width: 600px) {
  .main-image {
    max-width: 95%;
    margin-left: auto;
    margin-right: auto;
  }
  .object-row {
    flex-direction: column;
    align-items: flex-start;
  }
  button {
    margin-left: 0;
    margin-top: 10px;
    align-self: flex-end;
  }
}
</style>