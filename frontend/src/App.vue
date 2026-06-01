<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Sidebar -->
    <Sidebar
      :areas="areas"
      :selectedAreaId="selectedAreaId"
      :loading="areasLoading"
      @select-area="selectArea"
      @delete-area="showDeleteAreaConfirm"
      @new-area="showNewAreaModal = true"
    />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Header -->
      <Header :selectedArea="selectedArea" />

      <!-- Content -->
      <div v-if="selectedAreaId" class="flex-1 overflow-auto">
        <!-- Stats Bar -->
        <StatsBar :stats="stats" />

        <!-- Filters and Actions -->
        <FilterBar
          :filters="filters"
          @update:filters="updateFilters"
          @new-task="showNewTaskModal = true"
          @export-csv="exportTasks"
        />

        <!-- Tasks Table -->
        <TaskTable
          :tasks="tasks"
          :loading="tasksLoading"
          @toggle-status="toggleTaskStatus"
          @edit-task="editTask"
          @delete-task="showDeleteTaskConfirm"
        />
      </div>

      <!-- Empty State -->
      <EmptyState v-else />
    </div>

    <!-- Modals -->
    <AreaModal
      v-if="showNewAreaModal"
      :area="null"
      @close="showNewAreaModal = false"
      @save="saveArea"
    />

    <AreaModal
      v-if="areaToEdit"
      :area="areaToEdit"
      @close="areaToEdit = null"
      @save="saveArea"
    />

    <ConfirmModal
      v-if="areaToDelete"
      title="Delete Area"
      :message="`Are you sure you want to delete '${areaToDelete.name}'? All tasks in this area will be deleted.`"
      @close="areaToDelete = null"
      @confirm="confirmDeleteArea"
    />

    <TaskModal
      v-if="showNewTaskModal"
      :task="null"
      :area-id="selectedAreaId"
      @close="showNewTaskModal = false"
      @save="saveTask"
    />

    <TaskModal
      v-if="taskToEdit"
      :task="taskToEdit"
      :area-id="selectedAreaId"
      @close="taskToEdit = null"
      @save="saveTask"
    />

    <ConfirmModal
      v-if="taskToDelete"
      title="Delete Task"
      message="Are you sure you want to delete this task?"
      @close="taskToDelete = null"
      @confirm="confirmDeleteTask"
    />
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useAreas } from './composables/useAreas'
import { useTasks } from './composables/useTasks'
import Sidebar from './components/Sidebar.vue'
import Header from './components/Header.vue'
import StatsBar from './components/StatsBar.vue'
import FilterBar from './components/FilterBar.vue'
import TaskTable from './components/TaskTable.vue'
import EmptyState from './components/EmptyState.vue'
import AreaModal from './components/AreaModal.vue'
import TaskModal from './components/TaskModal.vue'
import ConfirmModal from './components/ConfirmModal.vue'

export default {
  components: {
    Sidebar,
    Header,
    StatsBar,
    FilterBar,
    TaskTable,
    EmptyState,
    AreaModal,
    TaskModal,
    ConfirmModal,
  },
  setup() {
    const {
      areas,
      loading: areasLoading,
      selectedAreaId,
      selectedArea,
      fetchAreas,
      createArea,
      updateArea,
      deleteArea,
      selectArea: selectAreaFn,
    } = useAreas()

    const {
      tasks,
      loading: tasksLoading,
      stats,
      fetchTasks,
      createTask,
      updateTask,
      deleteTask,
      toggleTaskStatus: toggleTaskStatusFn,
      exportToCSV,
    } = useTasks()

    // Modal states
    const showNewAreaModal = ref(false)
    const showNewTaskModal = ref(false)
    const areaToEdit = ref(null)
    const areaToDelete = ref(null)
    const taskToEdit = ref(null)
    const taskToDelete = ref(null)

    // Filter state
    const filters = ref({
      search: '',
      status: '',
      priority: '',
    })

    const updateFilters = (newFilters) => {
      filters.value = newFilters
      fetchTasks(selectedAreaId.value, newFilters)
    }

    const selectArea = (areaId) => {
      selectAreaFn(areaId)
      filters.value = { search: '', status: '', priority: '' }
      fetchTasks(areaId)
    }

    const saveArea = async (areaData) => {
      if (areaData.id) {
        await updateArea(areaData.id, areaData)
      } else {
        await createArea(areaData)
      }
      showNewAreaModal.value = false
      areaToEdit.value = null
    }

    const showDeleteAreaConfirm = (area) => {
      areaToDelete.value = area
    }

    const confirmDeleteArea = async () => {
      await deleteArea(areaToDelete.value.id)
      areaToDelete.value = null
    }

    const saveTask = async (taskData) => {
      if (taskData.id) {
        await updateTask(taskData.id, taskData)
      } else {
        await createTask(taskData)
      }
      showNewTaskModal.value = false
      taskToEdit.value = null
      fetchTasks(selectedAreaId.value, filters.value)
    }

    const editTask = (task) => {
      taskToEdit.value = task
    }

    const showDeleteTaskConfirm = (taskId) => {
      taskToDelete.value = taskId
    }

    const confirmDeleteTask = async () => {
      await deleteTask(taskToDelete.value)
      taskToDelete.value = null
      fetchTasks(selectedAreaId.value, filters.value)
    }

    const toggleTaskStatus = async (task) => {
      await toggleTaskStatusFn(task)
      fetchTasks(selectedAreaId.value, filters.value)
    }

    const exportTasks = () => {
      exportToCSV(tasks.value)
    }

    onMounted(() => {
      fetchAreas()
    })

    return {
      // Area state
      areas,
      areasLoading,
      selectedAreaId,
      selectedArea,
      selectArea,
      saveArea,
      showDeleteAreaConfirm,
      confirmDeleteArea,
      showNewAreaModal,
      areaToEdit,
      areaToDelete,

      // Task state
      tasks,
      tasksLoading,
      stats,
      filters,
      updateFilters,
      saveTask,
      editTask,
      showDeleteTaskConfirm,
      confirmDeleteTask,
      toggleTaskStatus,
      exportTasks,
      showNewTaskModal,
      taskToEdit,
      taskToDelete,
    }
  },
}
</script>

<script setup>
import { ref } from 'vue'
</script>
