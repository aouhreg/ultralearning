import { defineStore } from 'pinia'
import { goalsApi } from '@/api'

export const useGoalsStore = defineStore('goals', {
  state: () => ({
    goals: [],
    currentGoal: null,
    loading: false,
  }),
  actions: {
    async fetchGoals() {
      this.loading = true
      try { this.goals = await goalsApi.list() }
      finally { this.loading = false }
    },
    async createGoal(data) {
      const goal = await goalsApi.create(data)
      this.goals.unshift(goal)
      return goal
    },
    async fetchGoal(id) {
      this.currentGoal = await goalsApi.get(id)
      return this.currentGoal
    },
    async updateProgress(id, progress) {
      const updated = await goalsApi.updateProgress(id, progress)
      const idx = this.goals.findIndex(g => g.id === id)
      if (idx !== -1) this.goals[idx] = updated
      if (this.currentGoal?.id === id) this.currentGoal = updated
    }
  }
})
