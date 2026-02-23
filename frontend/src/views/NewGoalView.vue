<template>
  <div class="p-8 max-w-3xl mx-auto">
    <div class="mb-8">
      <h1 class="text-2xl font-bold">創建學習目標</h1>
      <p class="text-gray-400 mt-1">AI 將根據你的目標生成個性化學習路線圖</p>
    </div>

    <div class="card">
      <form @submit.prevent="handleCreate" class="space-y-6">
        <div>
          <label class="block text-sm font-medium mb-2">學習主題 *</label>
          <input v-model="form.topic" class="input" placeholder="例如：機器學習、西班牙語、吉他演奏、量子力學..." required />
        </div>
        <div>
          <label class="block text-sm font-medium mb-2">學習目標 *</label>
          <textarea v-model="form.goal" class="input resize-none" rows="3"
            placeholder="描述你希望達到的具體目標，例如：能夠獨立開發和部署深度學習模型，並在 Kaggle 競賽中進入前20%..." required />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium mb-2">可用總時間</label>
            <select v-model="form.timeAvailable" class="input">
              <option value="1個月">1 個月</option>
              <option value="3個月">3 個月</option>
              <option value="6個月">6 個月</option>
              <option value="12個月">12 個月</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">每天學習時間（小時）</label>
            <input v-model.number="form.dailyHours" type="number" class="input" min="0.5" max="12" step="0.5" />
          </div>
        </div>

        <!-- AI 生成提示 -->
        <div class="bg-primary/10 border border-primary/30 rounded-lg p-4 flex gap-3">
          <span class="text-2xl">🤖</span>
          <div>
            <p class="font-medium text-primary">AI 自動生成知識地圖</p>
            <p class="text-sm text-gray-400 mt-1">提交後，AI 將分析你的學習目標，自動生成包含核心概念、學習路線、資源推薦的完整知識地圖。</p>
          </div>
        </div>

        <div v-if="error" class="text-red-400 text-sm bg-red-900/20 rounded-lg p-3">{{ error }}</div>

        <div class="flex gap-3">
          <button type="submit" class="btn-primary flex-1 py-3" :disabled="loading">
            <span v-if="loading">🤖 AI 正在分析...</span>
            <span v-else>✨ 創建目標並生成學習計畫</span>
          </button>
          <router-link to="/dashboard" class="btn-secondary px-6 py-3">取消</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useGoalsStore } from '@/store/goals'

const goals = useGoalsStore()
const router = useRouter()
const form = ref({ topic: '', goal: '', timeAvailable: '3個月', dailyHours: 1.5 })
const loading = ref(false)
const error = ref('')

async function handleCreate() {
  loading.value = true
  error.value = ''
  try {
    const goal = await goals.createGoal(form.value)
    router.push(`/goals/${goal.id}`)
  } catch (e) {
    error.value = e?.message || '創建失敗，請重試'
  } finally {
    loading.value = false
  }
}
</script>
