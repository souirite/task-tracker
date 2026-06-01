import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Area endpoints
export const areasAPI = {
  getAll: () => api.get('/areas'),
  create: (data) => api.post('/areas', data),
  get: (id) => api.get(`/areas/${id}`),
  update: (id, data) => api.put(`/areas/${id}`, data),
  delete: (id) => api.delete(`/areas/${id}`),
}

// Task endpoints
export const tasksAPI = {
  getAll: (areaId, params = {}) => api.get('/tasks', {
    params: { area_id: areaId, ...params }
  }),
  create: (data) => api.post('/tasks', data),
  get: (id) => api.get(`/tasks/${id}`),
  update: (id, data) => api.put(`/tasks/${id}`, data),
  delete: (id) => api.delete(`/tasks/${id}`),
  getStats: (areaId) => api.get(`/tasks/stats/${areaId}`),
}

export default api
