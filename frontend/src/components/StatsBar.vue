<template>
  <div class="bg-white border-b border-gray-200 p-6">
    <div class="grid grid-cols-4 gap-4">
      <div class="bg-gray-50 p-4 rounded-lg">
        <p class="text-gray-500 text-sm">Total</p>
        <p class="text-3xl font-bold text-gray-900">{{ stats.total }}</p>
      </div>
      <div class="bg-green-50 p-4 rounded-lg">
        <p class="text-green-600 text-sm">Open</p>
        <p class="text-3xl font-bold text-green-600">{{ stats.open }}</p>
      </div>
      <div class="bg-gray-50 p-4 rounded-lg">
        <p class="text-gray-500 text-sm">Closed</p>
        <p class="text-3xl font-bold text-gray-900">{{ stats.closed }}</p>
      </div>
      <div class="bg-red-50 p-4 rounded-lg">
        <p class="text-red-600 text-sm">Critical</p>
        <p class="text-3xl font-bold text-red-600">{{ stats.critical }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    stats: {
      type: Object,
      default: () => ({
        total: 0,
        open: 0,
        closed: 0,
        critical: 0,
      }),
    },
  },
}
</script>
