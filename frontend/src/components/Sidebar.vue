<template>
  <div class="w-64 bg-white border-r border-gray-200 flex flex-col">
    <!-- Header -->
    <div class="p-6 border-b border-gray-200">
      <h1 class="text-2xl font-bold text-gray-900">Task Tracker</h1>
      <p class="text-sm text-gray-500 mt-1">Organize by areas</p>
    </div>

    <!-- Areas List -->
    <div class="flex-1 overflow-y-auto p-4">
      <div v-if="loading" class="text-gray-500 text-sm">Loading areas...</div>
      <div v-else-if="areas.length === 0" class="text-gray-500 text-sm">No areas yet</div>
      <div v-else class="space-y-2">
        <button
          v-for="area in areas"
          :key="area.id"
          @click="$emit('select-area', area.id)"
          :class="[
            'w-full text-left px-4 py-3 rounded-lg transition-colors',
            selectedAreaId === area.id
              ? 'bg-blue-100 text-blue-900 font-medium'
              : 'text-gray-700 hover:bg-gray-100'
          ]"
        >
          <div class="flex justify-between items-center">
            <span>{{ area.name }}</span>
            <button
              @click.stop="$emit('delete-area', area)"
              class="text-gray-400 hover:text-red-600 text-sm"
            >
              ×
            </button>
          </div>
        </button>
      </div>
    </div>

    <!-- New Area Button -->
    <div class="p-4 border-t border-gray-200">
      <button
        @click="$emit('new-area')"
        class="w-full btn btn-primary"
      >
        + New Area
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    areas: {
      type: Array,
      default: () => [],
    },
    selectedAreaId: {
      type: Number,
      default: null,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['select-area', 'delete-area', 'new-area'],
}
</script>
