<template>
  <div class="bg-white border-b border-gray-200 p-6">
    <div v-if="selectedArea">
      <h2 class="text-2xl font-bold text-gray-900">{{ selectedArea.name }}</h2>
      <p class="text-gray-500 mt-1">{{ selectedArea.description }}</p>
    </div>
    <div v-else class="text-gray-500">
      Select or create an area to get started
    </div>
  </div>
</template>

<script>
export default {
  props: {
    selectedArea: {
      type: Object,
      default: null,
    },
  },
}
</script>
