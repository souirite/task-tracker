import { ref, computed } from 'vue'
import { areasAPI } from '../api'

export function useAreas() {
  const areas = ref([])
  const loading = ref(false)
  const selectedAreaId = ref(null)

  const selectedArea = computed(() => {
    return areas.value.find(a => a.id === selectedAreaId.value)
  })

  const fetchAreas = async () => {
    loading.value = true
    try {
      const response = await areasAPI.getAll()
      areas.value = response.data
      if (areas.value.length > 0 && !selectedAreaId.value) {
        selectedAreaId.value = areas.value[0].id
      }
    } catch (error) {
      console.error('Error fetching areas:', error)
    } finally {
      loading.value = false
    }
  }

  const createArea = async (areaData) => {
    try {
      await areasAPI.create(areaData)
      await fetchAreas()
      return true
    } catch (error) {
      console.error('Error creating area:', error)
      return false
    }
  }

  const updateArea = async (areaId, areaData) => {
    try {
      await areasAPI.update(areaId, areaData)
      await fetchAreas()
      return true
    } catch (error) {
      console.error('Error updating area:', error)
      return false
    }
  }

  const deleteArea = async (areaId) => {
    try {
      await areasAPI.delete(areaId)
      if (selectedAreaId.value === areaId) {
        selectedAreaId.value = null
      }
      await fetchAreas()
      return true
    } catch (error) {
      console.error('Error deleting area:', error)
      return false
    }
  }

  const selectArea = (areaId) => {
    selectedAreaId.value = areaId
  }

  return {
    areas,
    loading,
    selectedAreaId,
    selectedArea,
    fetchAreas,
    createArea,
    updateArea,
    deleteArea,
    selectArea,
  }
}
