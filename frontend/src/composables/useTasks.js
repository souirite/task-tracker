import { ref } from 'vue'
import { tasksAPI } from '../api'

export function useTasks() {
  const tasks = ref([])
  const loading = ref(false)
  const stats = ref({ total: 0, open: 0, closed: 0, critical: 0 })

  const fetchTasks = async (areaId, filters = {}) => {
    if (!areaId) return
    loading.value = true
    try {
      const params = {}
      if (filters.search) params.search = filters.search
      if (filters.status) params.status = filters.status
      if (filters.priority) params.priority = filters.priority

      const response = await tasksAPI.getAll(areaId, params)
      tasks.value = response.data
      await fetchStats(areaId)
    } catch (error) {
      console.error('Error fetching tasks:', error)
    } finally {
      loading.value = false
    }
  }

  const fetchStats = async (areaId) => {
    if (!areaId) return
    try {
      const response = await tasksAPI.getStats(areaId)
      stats.value = response.data
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  const createTask = async (taskData) => {
    try {
      await tasksAPI.create(taskData)
      return true
    } catch (error) {
      console.error('Error creating task:', error)
      return false
    }
  }

  const updateTask = async (taskId, taskData) => {
    try {
      await tasksAPI.update(taskId, taskData)
      return true
    } catch (error) {
      console.error('Error updating task:', error)
      return false
    }
  }

  const deleteTask = async (taskId) => {
    try {
      await tasksAPI.delete(taskId)
      return true
    } catch (error) {
      console.error('Error deleting task:', error)
      return false
    }
  }

  const toggleTaskStatus = async (task) => {
    const newStatus = task.status === 'open' ? 'closed' : 'open'
    const dateClosed = newStatus === 'closed' ? new Date() : null
    return updateTask(task.id, {
      status: newStatus,
      date_closed: dateClosed,
    })
  }

  const exportToCSV = (tasks) => {
    const headers = ['ID', 'Description', 'Priority', 'Status', 'Date Raised', 'Date Closed']
    const rows = tasks.map(task => [
      task.id,
      task.description,
      task.priority,
      task.status,
      new Date(task.date_raised).toLocaleDateString(),
      task.date_closed ? new Date(task.date_closed).toLocaleDateString() : '-',
    ])

    const csv = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(',')),
    ].join('\n')

    const blob = new Blob([csv], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `tasks-${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    window.URL.revokeObjectURL(url)
  }

  return {
    tasks,
    loading,
    stats,
    fetchTasks,
    fetchStats,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskStatus,
    exportToCSV,
  }
}
