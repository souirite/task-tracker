<template>
  <div class="p-6">
    <div v-if="loading" class="text-center text-gray-500">Loading tasks...</div>
    <div v-else-if="tasks.length === 0" class="text-center text-gray-500 py-8">
      No tasks found
    </div>
    <div v-else class="overflow-x-auto">
      <table class="w-full">
        <thead>
          <tr class="border-b border-gray-200 bg-gray-50">
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">ID</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">Description</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">Priority</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">Status</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">Date Raised</th>
            <th class="px-4 py-3 text-left text-sm font-semibold text-gray-700">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in tasks" :key="task.id" class="table-row">
            <td class="px-4 py-3 text-sm text-gray-900">#{{ task.id }}</td>
            <td class="px-4 py-3 text-sm text-gray-900">{{ task.description }}</td>
            <td class="px-4 py-3 text-sm">
              <span :class="getPriorityClass(task.priority)">
                {{ task.priority }}
              </span>
            </td>
            <td class="px-4 py-3 text-sm">
              <button
                @click="$emit('toggle-status', task)"
                :class="[
                  'px-3 py-1 rounded-full text-sm font-medium',
                  task.status === 'open'
                    ? 'bg-green-100 text-green-700'
                    : 'bg-gray-100 text-gray-700'
                ]"
              >
                {{ task.status }}
              </button>
            </td>
            <td class="px-4 py-3 text-sm text-gray-600">
              {{ formatDate(task.date_raised) }}
            </td>
            <td class="px-4 py-3 text-sm">
              <button
                @click="$emit('edit-task', task)"
                class="text-blue-600 hover:text-blue-900 mr-3"
              >
                Edit
              </button>
              <button
                @click="$emit('delete-task', task.id)"
                class="text-red-600 hover:text-red-900"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    tasks: {
      type: Array,
      default: () => [],
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['toggle-status', 'edit-task', 'delete-task'],
  methods: {
    formatDate(date) {
      return new Date(date).toLocaleDateString()
    },
    getPriorityClass(priority) {
      const classes = {
        Critical: 'bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm font-medium',
        High: 'bg-orange-100 text-orange-700 px-3 py-1 rounded-full text-sm font-medium',
        Medium: 'bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium',
        Low: 'bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-medium',
      }
      return classes[priority] || classes.Medium
    },
  },
}
</script>
