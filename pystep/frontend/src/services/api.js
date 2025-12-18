import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para adicionar token
api.interceptors.request.use((config) => {
  const token = JSON.parse(localStorage.getItem('pystep-auth'))?.state?.token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
}

// Lessons
export const lessonsAPI = {
  getAll: (nivel) => api.get('/lessons', { params: { nivel } }),
  getById: (id) => api.get(`/lessons/${id}`),
  // Novo endpoint: lições com progresso do usuário
  getAllWithProgress: (userId) => api.get(`/lessons/user/${userId}`),
}

// Exercises
export const exercisesAPI = {
  getById: (id) => api.get(`/exercises/${id}`),
  getByLesson: (lessonId) => api.get('/exercises', { params: { lesson_id: lessonId } }),
}

// Execute
export const executeAPI = {
  run: (data) => api.post('/execute', data),
  getHint: (exerciseId, code) => api.post('/execute/hint', { 
    exercise_id: exerciseId, 
    current_code: code 
  }),
}

// Progress
export const progressAPI = {
  getUser: (userId) => api.get(`/progress/${userId}`),
  markComplete: (userId, lessonId) => api.post('/progress/complete', { 
    user_id: userId, 
    lesson_id: lessonId 
  }),
}

export default api
