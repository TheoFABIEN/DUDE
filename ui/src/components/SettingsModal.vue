<script setup>
const emits = defineEmits(['close'])
function close() {
    emits("close")
}
</script>


<template>
    <div class="modal-overlay" @click.self="close">
        <div class="modal">
            <h3>Family filter</h3>
            <i>Feature available soon</i>
            <div class="modal-actions">
              <button @click="Apply">Apply</button>
              <button @click="close">Cancel</button>
            </div>
        </div>
    </div>
</template>


<style scoped>
.modal {
    padding: 20px;
    width: 300px;
    text-align: center;
}
.modal-actions {
    margin-top: 15px;
    display: flex;
    justify-content: space-around;
}
</style>