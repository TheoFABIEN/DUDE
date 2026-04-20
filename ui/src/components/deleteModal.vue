<script setup>
const emit = defineEmits(['confirm', 'cancel'])
</script>


<template>
    <div class="modal-overlay">
      <div class="modal">
        <p>Are you sure you want to delete this box?</p>

        <div class="modal-actions">
          <button @click="emit('confirm')">Yes</button>
          <button @click="emit('cancel')">Cancel</button>
        </div>
      </div>
    </div>
</template>

<style scoped>
.delete-btn {
  background: #ff4d4f;
  color: white;
  border: none;
  padding: 6px 10px;
  border-radius: 6px;
  cursor: pointer;
}

.delete-btn:hover {
  background: #d9363e;
}

/* modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 3000;
}

.modal {
  background: var(--ui-anthracite);
  padding: 20px;
  border-radius: 10px;
  width: 300px;
  text-align: center;
}

.modal-actions {
  margin-top: 15px;
  display: flex;
  justify-content: space-around;
}
</style>