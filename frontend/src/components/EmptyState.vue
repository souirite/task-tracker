<template>
  <div class="flex-1 flex items-center justify-center text-gray-500">
    <div class="text-center">
      <p class="text-lg">{{ message }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    message: {
      type: String,
      default: 'Select or create an area to get started',
    },
  },
}
</script>
