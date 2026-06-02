import axios from 'axios'

const API_BASE_URL = '/api'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Prediction API
export const predictPerformance = async (studentData) => {
  const response = await api.post('/predictions', studentData)
  return response.data
}

export const batchPredict = async (studentDataArray) => {
  const response = await api.post('/batch-predictions', studentDataArray)
  return response.data
}

// Model API
export const getModelInfo = async () => {
  const response = await api.get('/models/info')
  return response.data
}

export const getFeatureImportance = async () => {
  const response = await api.get('/models/feature-importance')
  return response.data
}

export const getModelMetrics = async () => {
  const response = await api.get('/models/metrics')
  return response.data
}

// Health check
export const healthCheck = async () => {
  const response = await api.get('/health')
  return response.data
}

export default api
