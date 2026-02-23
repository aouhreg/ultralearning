import { defineStore } from 'pinia'
import { authApi } from '@/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user') || 'null'),
  }),
  getters: {
    isLoggedIn: s => !!s.token,
  },
  actions: {
    async login(credentials) {
      const data = await authApi.login(credentials)
      this.token = data.token
      this.user = { id: data.userId, username: data.username, displayName: data.displayName, email: data.email }
      localStorage.setItem('token', data.token)
      localStorage.setItem('user', JSON.stringify(this.user))
    },
    async register(data) {
      const res = await authApi.register(data)
      this.token = res.token
      this.user = { id: res.userId, username: res.username, displayName: res.displayName, email: res.email }
      localStorage.setItem('token', res.token)
      localStorage.setItem('user', JSON.stringify(this.user))
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
})
