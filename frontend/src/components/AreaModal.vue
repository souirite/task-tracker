<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <div class="p-6 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">
          {{ area ? 'Edit Area' : 'New Area' }}
        </h3>
      </div>

      <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Area Name *
          </label>
          <input
            v-model="formData.name"
            type="text"
            required
            class="input"
            placeholder="Enter area name"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Description
          </label>
          <textarea
            v-model="formData.description"
            class="input"
            placeholder="Enter area description"
            rows="3"
          ></textarea>
        </div>

        <div class="flex gap-3 pt-4">
          <button
            type="submit"
            class="btn btn-primary flex-1"
          >
            Save
          </button>
          <button
            type="button"
            @click="$emit('close')"
            class="btn btn-secondary flex-1"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    area: {
      type: Object,
      default: null,
    },
  },
  emits: ['close', 'save'],
  data() {
    return {
      formData: {
        name: '',
        description: '',
      },
    }
  },
  watch: {
    area: {
      handler(newArea) {
        if (newArea) {
          this.formData = { ...newArea }
        } else {
          this.formData = { name: '', description: '' }
        }
      },
      immediate: true,
    },
  },
  methods: {
    handleSubmit() {
      this.$emit('save', this.formData)
    },
  },
}
</script>
