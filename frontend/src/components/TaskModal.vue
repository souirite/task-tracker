<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal max-w-lg">
      <div class="p-6 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">
          {{ task ? 'Edit Task' : 'New Task' }}
        </h3>
      </div>

      <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Description *
          </label>
          <textarea
            v-model="formData.description"
            required
            class="input"
            placeholder="Enter task description"
            rows="3"
          ></textarea>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Priority
            </label>
            <select v-model="formData.priority" class="select">
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Status
            </label>
            <select v-model="formData.status" class="select">
              <option value="open">Open</option>
              <option value="closed">Closed</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Date Raised *
            </label>
            <input
              v-model="formData.date_raised"
              type="datetime-local"
              required
              class="input"
            />
          </div>

          <div v-if="formData.status === 'closed'">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Date Closed
            </label>
            <input
              v-model="formData.date_closed"
              type="datetime-local"
              class="input"
            />
          </div>
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
    task: {
      type: Object,
      default: null,
    },
    areaId: {
      type: Number,
      required: true,
    },
  },
  emits: ['close', 'save'],
  data() {
    return {
      formData: {
        area_id: this.areaId,
        description: '',
        priority: 'Medium',
        status: 'open',
        date_raised: new Date().toISOString().slice(0, 16),
        date_closed: null,
      },
    }
  },
  watch: {
    task: {
      handler(newTask) {
        if (newTask) {
          this.formData = {
            ...newTask,
            date_raised: new Date(newTask.date_raised).toISOString().slice(0, 16),
            date_closed: newTask.date_closed
              ? new Date(newTask.date_closed).toISOString().slice(0, 16)
              : null,
          }
        } else {
          this.formData = {
            area_id: this.areaId,
            description: '',
            priority: 'Medium',
            status: 'open',
            date_raised: new Date().toISOString().slice(0, 16),
            date_closed: null,
          }
        }
      },
      immediate: true,
    },
  },
  methods: {
    handleSubmit() {
      const data = {
        ...this.formData,
        date_raised: new Date(this.formData.date_raised),
        date_closed: this.formData.date_closed
          ? new Date(this.formData.date_closed)
          : null,
      }
      this.$emit('save', data)
    },
  },
}
</script>
