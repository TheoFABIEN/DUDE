<script setup>
const props = defineProps({
  image: Object,
  imgIndex: Number,
  direction: String
})

const emit = defineEmits([
  'request-delete'
])

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
    <transition :name="direction === 'next' ? 'slide-left' : 'slide-right'" mode="out-in">
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
            <div class="actions">
              <button class="delete-btn" @click="emit('request-delete', props.imgIndex, i)">
                Delete
              </button>
              <button class="reset-btn" v-if="obj.edited" @click="resetClass(obj)">
                Reset
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>


<style scoped>

.slide-left-enter-active,
.slide-left-leave-active {
  transition: all 0.3s ease;
}
.slide-left-enter-from {
  transform: translateX(50px);
  opacity: 0;
}
.slide-left-leave-to {
  transform: translateX(-50px);
  opacity: 0;
}
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.3s ease;
}
.slide-right-enter-from {
  transform: translateX(-50px);
  opacity: 0;
}
.slide-right-leave-to {
  transform: translateX(50px);
  opacity: 0;
}

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
  align-items: flex-start;
  margin-bottom: 10px;
  &:hover {
    background-color: var(--ui-anthracite);
  }
}
.left {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: 10px;
}
.actions {
  display: flex;
  flex-direction: column;
  margin-left: auto;
  align-items: flex-end;
  gap: 6px;
  button {
    background: none;
  }
}

.delete-btn{
  color: #af3638;
  &:hover {
  color: #e93639;
  }
}
.reset-btn {
  color: var(--ui-grey);
  &:hover {
    color: var(--ui-amber);
  }
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

@media (max-width: 600px) {
  .main-image {
    max-width: 95%;
    margin-left: auto;
    margin-right: auto;
  }
  .object-row {
    flex-direction: column;
    align-items: flex-start;
    &:hover {
      background: none;
    }
  }
  .actions {
    flex-direction: row;
    justify-content: flex-end;
    align-items: center;
    min-height: auto;
    width: 100%;
    button {
      margin-left: 0;
      margin-top: 10px;
      align-self: flex-end;
    }
  }
  .reset-btn {
    order: 1;
  }
  .delete-btn {
    order: 2;
    margin-left: auto;
  }
}
</style>