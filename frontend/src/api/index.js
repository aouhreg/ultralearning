import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000,
})

// 自動附加 JWT Token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// 統一錯誤處理
api.interceptors.response.use(
  res => res.data,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(err.response?.data || err)
  }
)

// ── Auth ───────────────────────────────────────────────────────────────────
export const authApi = {
  register: data => api.post('/auth/register', data),
  login: data => api.post('/auth/login', data),
}

// ── Learning Goals ─────────────────────────────────────────────────────────
export const goalsApi = {
  create: data => api.post('/goals', data),
  list: () => api.get('/goals'),
  get: id => api.get(`/goals/${id}`),
  updateProgress: (id, progress) => api.put(`/goals/${id}/progress`, { progress }),
}

// ── Flashcards ─────────────────────────────────────────────────────────────
export const flashcardsApi = {
  generate: data => api.post('/flashcards/generate', data),
  getAll: goalId => api.get(`/flashcards/goal/${goalId}`),
  getDue: goalId => api.get(`/flashcards/goal/${goalId}/due`),
  getDueCount: goalId => api.get(`/flashcards/goal/${goalId}/due-count`),
  review: (id, difficulty_rating) => api.post(`/flashcards/${id}/review`, { difficulty_rating }),
}

// ── AI Endpoints ───────────────────────────────────────────────────────────
export const aiApi = {
  getDrillQuestions: data => api.post('/ai/drill/questions', data),
  analyzeWeakPoints: data => api.post('/ai/drill/analyze-weak-points', data),
  evaluateAnswer: data => api.post('/ai/feedback/evaluate', data),
  trackProgress: data => api.post('/ai/feedback/progress', data),
  feynmanExplain: data => api.post('/ai/intuition/feynman-explain', data),
  getAnalogies: data => api.post('/ai/intuition/analogies', data),
  recallQuiz: data => api.post('/ai/retrieval/recall-quiz', data),
}

export default api
