<template>
  <div class="p-8">
    <!-- Header -->
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold">歡迎回來，{{ auth.user?.displayName }} 👋</h1>
        <p class="text-gray-400 mt-1">繼續你的學習旅程</p>
      </div>
      <router-link to="/goals/new" class="btn-primary">+ 新增目標</router-link>
    </div>

    <!-- Skeleton Loading -->
    <template v-if="goals.loading">
      <div class="grid grid-cols-4 gap-4 mb-8">
        <div v-for="i in 4" :key="i" class="card">
          <div class="skeleton-shimmer h-8 w-16 mx-auto mb-2" />
          <div class="skeleton-shimmer h-3 w-20 mx-auto" />
        </div>
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div v-for="i in 4" :key="i" class="card">
          <div class="skeleton-shimmer h-5 w-40 mb-3" />
          <div class="skeleton-shimmer h-3 w-full mb-2" />
          <div class="skeleton-shimmer h-2 w-full mt-4" />
        </div>
      </div>
    </template>

    <template v-else>
      <!-- Stats Cards -->
      <div class="grid grid-cols-4 gap-4 mb-8">
        <div class="card text-center group hover:border-primary/40 transition-all duration-200">
          <p class="text-3xl font-bold text-primary">{{ goals.goals.length }}</p>
          <p class="text-gray-400 text-sm mt-1">學習目標</p>
        </div>
        <div class="card text-center hover:border-green-500/40 transition-all duration-200">
          <p class="text-3xl font-bold text-green-400">{{ activeGoals }}</p>
          <p class="text-gray-400 text-sm mt-1">進行中</p>
        </div>
        <div class="card text-center hover:border-yellow-500/40 transition-all duration-200">
          <p class="text-3xl font-bold text-yellow-400">{{ totalFlashcards }}</p>
          <p class="text-gray-400 text-sm mt-1">閃卡總數</p>
        </div>
        <div class="card text-center hover:border-purple-500/40 transition-all duration-200">
          <p class="text-3xl font-bold text-purple-400">{{ avgProgress }}%</p>
          <p class="text-gray-400 text-sm mt-1">平均進度</p>
        </div>
      </div>

      <!-- Progress Chart (show only if ≥2 goals) -->
      <div v-if="goals.goals.length >= 2" class="card mb-8">
        <h2 class="text-base font-semibold mb-5 flex items-center gap-2">
          <span class="w-2 h-2 bg-primary rounded-full inline-block"></span>
          學習進度總覽
        </h2>
        <Bar :data="chartData" :options="chartOptions" style="max-height: 180px;" />
      </div>

      <!-- Learning Goals -->
      <div class="mb-5 flex items-center justify-between">
        <h2 class="text-xl font-semibold">我的學習目標</h2>
        <span class="text-sm text-gray-500">{{ goals.goals.length }} 個目標</span>
      </div>

      <div v-if="goals.goals.length === 0" class="card text-center py-16">
        <div class="text-5xl mb-4">📚</div>
        <h3 class="text-xl font-semibold mb-2">還沒有學習目標</h3>
        <p class="text-gray-400 mb-6">設定你的第一個學習目標，讓 AI 幫你規劃學習路線</p>
        <router-link to="/goals/new" class="btn-primary">創建第一個目標</router-link>
      </div>

      <div v-else class="grid grid-cols-2 gap-4">
        <div v-for="goal in goals.goals" :key="goal.id"
             class="card card-hover cursor-pointer group"
             @click="router.push(`/goals/${goal.id}`)">
          <div class="flex items-start justify-between mb-3">
            <div class="flex-1 min-w-0 pr-3">
              <h3 class="font-semibold text-lg group-hover:text-primary transition-colors truncate">{{ goal.topic }}</h3>
              <p class="text-gray-400 text-sm mt-1 line-clamp-2">{{ goal.goal }}</p>
            </div>
            <span :class="statusBadge(goal.status)" class="badge shrink-0">{{ statusLabel(goal.status) }}</span>
          </div>

          <!-- Progress Bar -->
          <div class="mt-4">
            <div class="flex justify-between text-sm mb-1.5">
              <span class="text-gray-500">進度</span>
              <span class="font-medium" :class="progressColor(goal.overallProgress)">{{ goal.overallProgress }}%</span>
            </div>
            <div class="h-1.5 bg-surface rounded-full overflow-hidden">
              <div class="h-full rounded-full progress-bar"
                   :class="progressBarColor(goal.overallProgress)"
                   :style="`width: ${goal.overallProgress}%`" />
            </div>
          </div>

          <!-- Stats -->
          <div class="flex gap-4 mt-4 text-xs text-gray-500">
            <span>📝 {{ goal.totalSessions || 0 }} 次練習</span>
            <span>🗂 {{ goal.flashcardCount || 0 }} 張閃卡</span>
            <span v-if="goal.dailyHours">⏱ {{ goal.dailyHours }}h/天</span>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-2 mt-4 pt-4 border-t border-surface-border opacity-0 group-hover:opacity-100 transition-opacity" @click.stop>
            <router-link :to="`/goals/${goal.id}/drill`" class="btn-secondary text-xs py-1.5 flex-1 text-center">🎯 練習</router-link>
            <router-link :to="`/goals/${goal.id}/flashcards`" class="btn-secondary text-xs py-1.5 flex-1 text-center">🗂 閃卡</router-link>
            <router-link :to="`/goals/${goal.id}/intuition`" class="btn-secondary text-xs py-1.5 flex-1 text-center">💡 直覺</router-link>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useGoalsStore } from '@/store/goals'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip)

const auth = useAuthStore()
const goals = useGoalsStore()
const router = useRouter()

const activeGoals = computed(() => goals.goals.filter(g => g.status === 'ACTIVE').length)
const totalFlashcards = computed(() => goals.goals.reduce((s, g) => s + (g.flashcardCount || 0), 0))
const avgProgress = computed(() => {
  if (!goals.goals.length) return 0
  return Math.round(goals.goals.reduce((s, g) => s + g.overallProgress, 0) / goals.goals.length)
})

const chartData = computed(() => ({
  labels: goals.goals.map(g => g.topic.length > 14 ? g.topic.slice(0, 14) + '…' : g.topic),
  datasets: [{
    data: goals.goals.map(g => g.overallProgress),
    backgroundColor: goals.goals.map(g =>
      g.overallProgress >= 75 ? 'rgba(74, 222, 128, 0.7)' :
      g.overallProgress >= 40 ? 'rgba(99, 102, 241, 0.7)' :
                                 'rgba(251, 191, 36, 0.7)'
    ),
    borderColor: goals.goals.map(g =>
      g.overallProgress >= 75 ? '#4ade80' :
      g.overallProgress >= 40 ? '#6366f1' :
                                 '#fbbf24'
    ),
    borderWidth: 1,
    borderRadius: 6,
  }]
}))

const chartOptions = {
  indexAxis: 'y',
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false }, tooltip: { callbacks: { label: ctx => ` ${ctx.raw}%` } } },
  scales: {
    x: {
      min: 0, max: 100,
      grid: { color: 'rgba(61,61,92,0.5)' },
      ticks: { color: '#9ca3af', callback: v => `${v}%` },
    },
    y: {
      grid: { display: false },
      ticks: { color: '#d1d5db', font: { size: 12 } },
    },
  },
}

function statusBadge(status) {
  return {
    ACTIVE:     'bg-green-900/50 text-green-400',
    COMPLETED:  'bg-blue-900/50 text-blue-400',
    PAUSED:     'bg-yellow-900/50 text-yellow-400',
    ABANDONED:  'bg-red-900/50 text-red-400',
  }[status] || 'bg-gray-800 text-gray-400'
}
function statusLabel(status) {
  return { ACTIVE: '進行中', COMPLETED: '已完成', PAUSED: '暫停', ABANDONED: '放棄' }[status] || status
}
function progressColor(p) {
  return p >= 75 ? 'text-green-400' : p >= 40 ? 'text-primary' : 'text-yellow-400'
}
function progressBarColor(p) {
  return p >= 75 ? 'bg-green-400' : p >= 40 ? 'bg-primary' : 'bg-yellow-400'
}
</script>
