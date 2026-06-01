<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <div class="p-6 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">
          {{ title }}
        </h3>
      </div>

      <div class="p-6">
        <p class="text-gray-700 mb-6">{{ message }}</p>

        <div class="flex gap-3">
          <button
            @click="$emit('confirm')"
            class="btn btn-danger flex-1"
          >
            Delete
          </button>
          <button
            @click="$emit('close')"
            class="btn btn-secondary flex-1"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: 'Confirm Delete',
    },
    message: {
      type: String,
      default: 'Are you sure you want to delete this item?',
    },
  },
  emits: ['close', 'confirm'],
}
</script>
