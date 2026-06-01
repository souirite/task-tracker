<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Sidebar -->
    <div class="w-64 bg-white border-r border-gray-200 flex flex-col">
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
            @click="selectArea(area.id)"
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
                @click.stop="showDeleteAreaModal(area)"
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
          @click="showNewAreaModal = true"
          class="w-full btn btn-primary"
        >
          + New Area
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Header -->
      <div class="bg-white border-b border-gray-200 p-6">
        <div v-if="selectedAreaId && selectedArea">
          <h2 class="text-2xl font-bold text-gray-900">{{ selectedArea.name }}</h2>
          <p class="text-gray-500 mt-1">{{ selectedArea.description }}</p>
        </div>
        <div v-else class="text-gray-500">
          Select or create an area to get started
        </div>
      </div>

      <!-- Content -->
      <div v-if="selectedAreaId" class="flex-1 overflow-auto">
        <!-- Stats Bar -->
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

        <!-- Filters and Actions -->
        <div class="bg-white border-b border-gray-200 p-6">
          <div class="flex gap-4 items-center flex-wrap">
            <input
              v-model="filters.search"
              @input="fetchTasks"
              type="text"
              placeholder="Search tasks..."
              class="input flex-1 min-w-64"
            />
            <select
              v-model="filters.status"
              @change="fetchTasks"
              class="select w-40"
            >
              <option value="">All Status</option>
              <option value="open">Open</option>
              <option value="closed">Closed</option>
            </select>
            <select
              v-model="filters.priority"
              @change="fetchTasks"
              class="select w-40"
            >
              <option value="">All Priority</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
            <button
              @click="showNewTaskModal = true"
              class="btn btn-primary whitespace-nowrap"
            >
              + New Task
            </button>
            <button
              @click="exportToCSV"
              class="btn btn-secondary whitespace-nowrap"
            >
              Export CSV
            </button>
          </div>
        </div>

        <!-- Tasks Table -->
        <div class="p-6">
          <div v-if="tasksLoading" class="text-center text-gray-500">Loading tasks...</div>
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
                      @click="toggleTaskStatus(task)"
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
                      @click="editTask(task)"
                      class="text-blue-600 hover:text-blue-900 mr-3"
                    >
                      Edit
                    </button>
                    <button
                      @click="deleteTask(task.id)"
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
      </div>

      <div v-else class="flex-1 flex items-center justify-center text-gray-500">
        Select or create an area to get started
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { areasAPI, tasksAPI } from './api'

export default {
  setup() {
    const areas = ref([])
    const tasks = ref([])
    const selectedAreaId = ref(null)
    const loading = ref(false)
    const tasksLoading = ref(false)
    const showNewAreaModal = ref(false)
    const showNewTaskModal = ref(false)
    const areaToDelete = ref(null)
    const taskToEdit = ref(null)
    const stats = ref({ total: 0, open: 0, closed: 0, critical: 0 })
    const filters = ref({
      search: '',
      status: '',
      priority: '',
    })

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
          fetchTasks()
        }
      } catch (error) {
        console.error('Error fetching areas:', error)
      } finally {
        loading.value = false
      }
    }

    const fetchTasks = async () => {
      if (!selectedAreaId.value) return
      tasksLoading.value = true
      try {
        const params = {}
        if (filters.value.search) params.search = filters.value.search
        if (filters.value.status) params.status = filters.value.status
        if (filters.value.priority) params.priority = filters.value.priority
        
        const response = await tasksAPI.getAll(selectedAreaId.value, params)
        tasks.value = response.data
        fetchStats()
      } catch (error) {
        console.error('Error fetching tasks:', error)
      } finally {
        tasksLoading.value = false
      }
    }

    const fetchStats = async () => {
      if (!selectedAreaId.value) return
      try {
        const response = await tasksAPI.getStats(selectedAreaId.value)
        stats.value = response.data
      } catch (error) {
        console.error('Error fetching stats:', error)
      }
    }

    const selectArea = (areaId) => {
      selectedAreaId.value = areaId
      filters.value = { search: '', status: '', priority: '' }
      fetchTasks()
    }

    const editTask = (task) => {
      taskToEdit.value = task
    }

    const deleteTask = async (taskId) => {
      if (confirm('Are you sure you want to delete this task?')) {
        try {
          await tasksAPI.delete(taskId)
          fetchTasks()
        } catch (error) {
          console.error('Error deleting task:', error)
        }
      }
    }

    const toggleTaskStatus = async (task) => {
      try {
        const newStatus = task.status === 'open' ? 'closed' : 'open'
        const dateClosed = newStatus === 'closed' ? new Date() : null
        await tasksAPI.update(task.id, {
          status: newStatus,
          date_closed: dateClosed,
        })
        fetchTasks()
      } catch (error) {
        console.error('Error updating task status:', error)
      }
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString()
    }

    const getPriorityClass = (priority) => {
      const classes = {
        Critical: 'bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm font-medium',
        High: 'bg-orange-100 text-orange-700 px-3 py-1 rounded-full text-sm font-medium',
        Medium: 'bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium',
        Low: 'bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-medium',
      }
      return classes[priority] || classes.Medium
    }

    const exportToCSV = () => {
      const headers = ['ID', 'Description', 'Priority', 'Status', 'Date Raised', 'Date Closed']
      const rows = tasks.value.map(task => [
        task.id,
        task.description,
        task.priority,
        task.status,
        formatDate(task.date_raised),
        task.date_closed ? formatDate(task.date_closed) : '-',
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

    onMounted(() => {
      fetchAreas()
    })

    return {
      areas,
      tasks,
      selectedAreaId,
      selectedArea,
      loading,
      tasksLoading,
      showNewAreaModal,
      showNewTaskModal,
      areaToDelete,
      taskToEdit,
      stats,
      filters,
      selectArea,
      editTask,
      deleteTask,
      toggleTaskStatus,
      formatDate,
      getPriorityClass,
      exportToCSV,
      fetchTasks,
    }
  },
}
</script>
