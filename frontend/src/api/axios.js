/**
 * Axios instance configuration
 * Centralized API client for all backend communication
 */

import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Response interceptor for error handling
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.status, error.response.data)
    } else if (error.request) {
      // Request made but no response
      console.error('No response from server:', error.request)
    } else {
      // Error in request setup
      console.error('Request error:', error.message)
    }
    return Promise.reject(error)
  }
)

export default apiClient