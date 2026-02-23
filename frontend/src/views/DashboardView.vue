<template>
  <div class="p-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold">歡迎回來，{{ auth.user?.displayName }} 👋</h1>
      <p class="text-gray-400 mt-1">繼續你的學習旅程</p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-4 gap-4 mb-8">
      <div class="card text-center">
        <p class="text-3xl font-bold text-primary">{{ goals.goals.length }}</p>
        <p class="text-gray-400 text-sm mt-1">學習目標</p>
      </div>
      <div class="card text-center">
        <p class="text-3xl font-bold text-green-400">{{ activeGoals }}</p>
        <p class="text-gray-400 text-sm mt-1">進行中</p>
      </div>
      <div class="card text-center">
        <p class="text-3xl font-bold text-yellow-400">{{ totalFlashcards }}</p>
        <p class="text-gray-400 text-sm mt-1">閃卡總數</p>
      </div>
      <div class="card text-center">
        <p class="text-3xl font-bold text-purple-400">{{ avgProgress }}%</p>
        <p class="text-gray-400 text-sm mt-1">平均進度</p>
      </div>
    </div>

    <!-- Learning Goals -->
    <div class="mb-6 flex items-center justify-between">
      <h2 class="text-xl font-semibold">我的學習目標</h2>
      <router-link to="/goals/new" class="btn-primary text-sm">+ 新增目標</router-link>
    </div>

    <div v-if="goals.loading" class="text-center py-20 text-gray-500">載入中...</div>

    <div v-else-if="goals.goals.length === 0" class="card text-center py-16">
      <div class="text-5xl mb-4">📚</div>
      <h3 class="text-xl font-semibold mb-2">還沒有學習目標</h3>
      <p class="text-gray-400 mb-6">設定你的第一個學習目標，讓 AI 幫你規劃學習路線</p>
      <router-link to="/goals/new" class="btn-primary">創建第一個目標</router-link>
    </div>

    <div v-else class="grid grid-cols-2 gap-4">
      <div v-for="goal in goals.goals" :key="goal.id"
           class="card hover:border-primary/50 transition-colors cursor-pointer group"
           @click="router.push(`/goals/${goal.id}`)">
        <div class="flex items-start justify-between mb-3">
          <div>
            <h3 class="font-semibold text-lg group-hover:text-primary transition-colors">{{ goal.topic }}</h3>
            <p class="text-gray-400 text-sm mt-1 line-clamp-2">{{ goal.goal }}</p>
          </div>
          <span :class="statusBadge(goal.status)" class="badge ml-3 shrink-0">{{ statusLabel(goal.status) }}</span>
        </div>

        <!-- Progress Bar -->
        <div class="mt-4">
          <div class="flex justify-between text-sm mb-1">
            <span class="text-gray-400">進度</span>
            <span class="text-white font-medium">{{ goal.overallProgress }}%</span>
          </div>
          <div class="h-2 bg-surface rounded-full overflow-hidden">
            <div class="h-full bg-primary progress-bar rounded-full" :style="`width: ${goal.overallProgress}%`" />
          </div>
        </div>

        <!-- Stats -->
        <div class="flex gap-4 mt-4 text-sm text-gray-500">
          <span>📝 {{ goal.totalSessions }} 次練習</span>
          <span>🗂 {{ goal.flashcardCount }} 張閃卡</span>
          <span v-if="goal.dailyHours">⏱ {{ goal.dailyHours }}h/天</span>
        </div>

        <!-- Action Buttons -->
        <div class="flex gap-2 mt-4 opacity-0 group-hover:opacity-100 transition-opacity" @click.stop>
          <router-link :to="`/goals/${goal.id}/drill`" class="btn-secondary text-xs py-1.5">🎯 練習</router-link>
          <router-link :to="`/goals/${goal.id}/flashcards`" class="btn-secondary text-xs py-1.5">🗂 閃卡</router-link>
          <router-link :to="`/goals/${goal.id}/intuition`" class="btn-secondary text-xs py-1.5">💡 直覺</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useGoalsStore } from '@/store/goals'

const auth = useAuthStore()
const goals = useGoalsStore()
const router = useRouter()

const activeGoals = computed(() => goals.goals.filter(g => g.status === 'ACTIVE').length)
const totalFlashcards = computed(() => goals.goals.reduce((s, g) => s + (g.flashcardCount || 0), 0))
const avgProgress = computed(() => {
  if (!goals.goals.length) return 0
  return Math.round(goals.goals.reduce((s, g) => s + g.overallProgress, 0) / goals.goals.length)
})

function statusBadge(status) {
  return {
    ACTIVE: 'bg-green-900/50 text-green-400',
    COMPLETED: 'bg-blue-900/50 text-blue-400',
    PAUSED: 'bg-yellow-900/50 text-yellow-400',
    ABANDONED: 'bg-red-900/50 text-red-400',
  }[status] || 'bg-gray-800 text-gray-400'
}
function statusLabel(status) {
  return { ACTIVE: '進行中', COMPLETED: '已完成', PAUSED: '暫停', ABANDONED: '放棄' }[status] || status
}
</script>
