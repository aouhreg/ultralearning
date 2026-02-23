<template>
  <div class="p-8" v-if="goal">
    <!-- Header -->
    <div class="flex items-start justify-between mb-8">
      <div>
        <div class="flex items-center gap-2 text-gray-500 text-sm mb-2">
          <router-link to="/dashboard" class="hover:text-white">儀表板</router-link>
          <span>/</span>
          <span class="text-white">{{ goal.topic }}</span>
        </div>
        <h1 class="text-2xl font-bold">{{ goal.topic }}</h1>
        <p class="text-gray-400 mt-1">{{ goal.goal }}</p>
      </div>
      <div class="flex gap-2">
        <router-link :to="`/goals/${goal.id}/drill`" class="btn-primary">🎯 開始練習</router-link>
      </div>
    </div>

    <!-- Progress & Stats -->
    <div class="grid grid-cols-4 gap-4 mb-8">
      <div class="card col-span-2">
        <p class="text-sm text-gray-400 mb-2">整體進度</p>
        <div class="flex items-center gap-4">
          <div class="flex-1">
            <div class="h-3 bg-surface rounded-full overflow-hidden">
              <div class="h-full bg-primary progress-bar rounded-full" :style="`width: ${goal.overallProgress}%`" />
            </div>
          </div>
          <span class="text-2xl font-bold text-primary">{{ goal.overallProgress }}%</span>
        </div>
        <div class="flex gap-2 mt-4">
          <button v-for="p in [25,50,75,100]" :key="p"
            @click="updateProgress(p)"
            :class="goal.overallProgress === p
              ? 'border-primary text-primary bg-primary/10'
              : 'border-surface-border text-gray-500 hover:border-primary hover:text-primary'"
            class="text-xs px-3 py-1.5 rounded-full border transition-all duration-150">
            {{ p }}%
          </button>
        </div>
      </div>
      <div class="card text-center">
        <p class="text-3xl font-bold text-blue-400">{{ goal.totalSessions || 0 }}</p>
        <p class="text-gray-400 text-sm mt-1">學習次數</p>
      </div>
      <div class="card text-center">
        <p class="text-3xl font-bold text-purple-400">{{ goal.flashcardCount || 0 }}</p>
        <p class="text-gray-400 text-sm mt-1">閃卡數量</p>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="grid grid-cols-3 gap-4 mb-8">
      <router-link :to="`/goals/${goal.id}/drill`" class="card hover:border-primary/50 transition-colors text-center cursor-pointer group">
        <div class="text-4xl mb-3">🎯</div>
        <h3 class="font-semibold group-hover:text-primary">刻意練習</h3>
        <p class="text-gray-400 text-sm mt-1">AI 生成針對性練習題，識別薄弱點</p>
      </router-link>
      <router-link :to="`/goals/${goal.id}/flashcards`" class="card hover:border-primary/50 transition-colors text-center cursor-pointer group">
        <div class="text-4xl mb-3">🗂</div>
        <h3 class="font-semibold group-hover:text-primary">間隔重複</h3>
        <p class="text-gray-400 text-sm mt-1">智能閃卡系統，科學安排複習時間</p>
      </router-link>
      <router-link :to="`/goals/${goal.id}/intuition`" class="card hover:border-primary/50 transition-colors text-center cursor-pointer group">
        <div class="text-4xl mb-3">💡</div>
        <h3 class="font-semibold group-hover:text-primary">費曼技巧</h3>
        <p class="text-gray-400 text-sm mt-1">深度理解概念，培養學習直覺</p>
      </router-link>
    </div>

    <!-- Knowledge Map -->
    <div v-if="knowledgeMap" class="card">
      <h2 class="text-xl font-semibold mb-6 flex items-center gap-2">
        <span>🗺️</span> 知識地圖
      </h2>

      <p class="text-gray-400 mb-6">{{ knowledgeMap.overview }}</p>

      <!-- Core Concepts -->
      <div class="mb-6">
        <h3 class="font-medium text-gray-300 mb-3">核心概念</h3>
        <div class="flex flex-wrap gap-2">
          <span v-for="concept in knowledgeMap.concepts" :key="concept.name"
            class="badge text-sm py-1.5 px-3"
            :class="importanceBadge(concept.importance)">
            {{ concept.name }}
          </span>
        </div>
      </div>

      <!-- Learning Path -->
      <div v-if="knowledgeMap.learning_path?.length" class="mb-6">
        <h3 class="font-medium text-gray-300 mb-3">學習路線</h3>
        <div class="space-y-3">
          <div v-for="week in knowledgeMap.learning_path.slice(0, 4)" :key="week.week"
               class="flex gap-4 p-3 bg-surface rounded-lg">
            <div class="w-8 h-8 bg-primary/20 text-primary rounded-full flex items-center justify-center text-sm font-bold shrink-0">
              {{ week.week }}
            </div>
            <div>
              <p class="font-medium">{{ week.focus }}</p>
              <ul class="text-sm text-gray-400 mt-1 space-y-0.5">
                <li v-for="task in week.tasks?.slice(0, 3)" :key="task">• {{ task }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Resources -->
      <div v-if="knowledgeMap.resources?.length">
        <h3 class="font-medium text-gray-300 mb-3">推薦資源</h3>
        <div class="grid grid-cols-2 gap-3">
          <div v-for="r in knowledgeMap.resources.slice(0, 4)" :key="r.name"
               class="flex gap-3 p-3 bg-surface rounded-lg">
            <span class="text-xl">{{ resourceIcon(r.type) }}</span>
            <div>
              <p class="font-medium text-sm">{{ r.name }}</p>
              <p class="text-gray-400 text-xs mt-0.5">{{ r.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="p-8 text-center text-gray-500">載入中...</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useGoalsStore } from '@/store/goals'

const route = useRoute()
const router = useRouter()
const goals = useGoalsStore()
const goal = ref(null)

const knowledgeMap = computed(() => {
  if (!goal.value?.knowledgeMapJson) return null
  try { return JSON.parse(goal.value.knowledgeMapJson) } catch { return null }
})

onMounted(async () => {
  goal.value = await goals.fetchGoal(route.params.id)
})

async function updateProgress(p) {
  await goals.updateProgress(goal.value.id, p)
  goal.value.overallProgress = p
}

function importanceBadge(imp) {
  return {
    high: 'bg-red-900/40 text-red-400',
    medium: 'bg-yellow-900/40 text-yellow-400',
    low: 'bg-gray-800 text-gray-400',
  }[imp] || 'bg-gray-800 text-gray-400'
}

function resourceIcon(type) {
  return { book: '📖', course: '🎓', website: '🌐' }[type] || '📌'
}
</script>
