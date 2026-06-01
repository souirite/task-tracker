<template>
  <div class="bg-white border-b border-gray-200 p-6">
    <div class="flex gap-4 items-center flex-wrap">
      <input
        :value="filters.search"
        @input="$emit('update:filters', { ...filters, search: $event.target.value })"
        type="text"
        placeholder="Search tasks..."
        class="input flex-1 min-w-64"
      />
      <select
        :value="filters.status"
        @change="$emit('update:filters', { ...filters, status: $event.target.value })"
        class="select w-40"
      >
        <option value="">All Status</option>
        <option value="open">Open</option>
        <option value="closed">Closed</option>
      </select>
      <select
        :value="filters.priority"
        @change="$emit('update:filters', { ...filters, priority: $event.target.value })"
        class="select w-40"
      >
        <option value="">All Priority</option>
        <option value="Critical">Critical</option>
        <option value="High">High</option>
        <option value="Medium">Medium</option>
        <option value="Low">Low</option>
      </select>
      <button
        @click="$emit('new-task')"
        class="btn btn-primary whitespace-nowrap"
      >
        + New Task
      </button>
      <button
        @click="$emit('export-csv')"
        class="btn btn-secondary whitespace-nowrap"
      >
        Export CSV
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    filters: {
      type: Object,
      default: () => ({
        search: '',
        status: '',
        priority: '',
      }),
    },
  },
  emits: ['update:filters', 'new-task', 'export-csv'],
}
</script>
