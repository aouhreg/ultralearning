<template>
  <div class="p-8 max-w-3xl mx-auto">
    <div class="mb-6 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <router-link :to="`/goals/${route.params.id}`" class="text-gray-500 hover:text-white">←</router-link>
        <h1 class="text-2xl font-bold">🗂 間隔重複閃卡</h1>
      </div>
      <button @click="showGenerate = true" class="btn-secondary text-sm">+ 生成閃卡</button>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-3 gap-4 mb-6">
      <div class="card text-center">
        <p class="text-2xl font-bold">{{ allCards.length }}</p>
        <p class="text-gray-400 text-sm">總閃卡數</p>
      </div>
      <div class="card text-center">
        <p class="text-2xl font-bold text-yellow-400">{{ dueCards.length }}</p>
        <p class="text-gray-400 text-sm">今日待複習</p>
      </div>
      <div class="card text-center">
        <p class="text-2xl font-bold text-green-400">{{ reviewedToday }}</p>
        <p class="text-gray-400 text-sm">今日已複習</p>
      </div>
    </div>

    <!-- Review Mode -->
    <div v-if="reviewMode && dueCards.length > 0">
      <!-- Progress -->
      <div class="flex items-center gap-3 mb-4">
        <span class="text-sm text-gray-400">{{ reviewIdx + 1 }} / {{ dueCards.length }}</span>
        <div class="flex-1 h-2 bg-surface-card rounded-full overflow-hidden">
          <div class="h-full bg-primary progress-bar rounded-full"
            :style="`width: ${(reviewIdx / dueCards.length) * 100}%`" />
        </div>
      </div>

      <!-- Flashcard 3D Flip -->
      <div class="flip-card mb-4" style="height: 260px;" @click="showAnswer = !showAnswer">
        <div class="flip-card-inner" :class="{ flipped: showAnswer }">
          <!-- Front -->
          <div class="flip-card-front bg-surface-card border border-surface-border cursor-pointer select-none">
            <p class="text-xs text-primary/70 uppercase tracking-widest font-semibold mb-5">問題</p>
            <p class="text-xl font-medium leading-relaxed">{{ currentCard.front }}</p>
            <div class="absolute bottom-5 flex items-center gap-1.5 text-gray-600 text-xs">
              <span>點擊翻轉</span>
              <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            </div>
          </div>
          <!-- Back -->
          <div class="flip-card-back bg-surface-card border border-green-500/30 cursor-pointer select-none">
            <p class="text-xs text-green-400/70 uppercase tracking-widest font-semibold mb-5">答案</p>
            <p class="text-xl font-medium text-green-300 leading-relaxed">{{ currentCard.back }}</p>
            <p v-if="currentCard.memoryTip" class="absolute bottom-5 text-sm text-primary/80 italic px-4">💡 {{ currentCard.memoryTip }}</p>
          </div>
        </div>
      </div>

      <!-- Rating Buttons -->
      <div v-if="showAnswer" class="grid grid-cols-4 gap-3">
        <button v-for="r in ratings" :key="r.value"
          @click="rateCard(r.value)"
          :class="r.cls"
          class="py-3 rounded-lg font-medium text-sm transition-colors">
          <div>{{ r.label }}</div>
          <div class="text-xs opacity-70">{{ r.desc }}</div>
        </button>
      </div>

      <div v-if="dueCards.length === 0 || reviewIdx >= dueCards.length"
           class="text-center mt-6">
        <p class="text-green-400 font-semibold">🎉 今日複習完成！</p>
        <button @click="exitReview" class="btn-secondary mt-3">返回</button>
      </div>
    </div>

    <!-- Card List / Start Review -->
    <div v-else>
      <div v-if="dueCards.length > 0" class="card mb-6 border-yellow-500/30">
        <div class="flex items-center justify-between">
          <div>
            <p class="font-semibold text-yellow-400">📅 今日需複習 {{ dueCards.length }} 張</p>
            <p class="text-gray-400 text-sm mt-1">科學安排的間隔重複，鞏固長期記憶</p>
          </div>
          <button @click="startReview" class="btn-primary">開始複習</button>
        </div>
      </div>

      <div v-else-if="allCards.length > 0" class="card mb-6 border-green-500/30 text-center p-6">
        <p class="text-green-400 font-semibold">✅ 今日複習全部完成！</p>
        <p class="text-gray-400 text-sm mt-1">做得很好，明天繼續保持</p>
      </div>

      <!-- All Cards -->
      <div class="space-y-3">
        <div v-for="card in allCards" :key="card.id"
             class="flex items-center gap-4 p-4 bg-surface-card rounded-lg border border-surface-border">
          <div class="flex-1">
            <p class="font-medium text-sm">{{ card.front }}</p>
            <p class="text-gray-500 text-sm mt-1 truncate">{{ card.back }}</p>
          </div>
          <div class="text-right text-xs text-gray-500 shrink-0">
            <p>{{ card.totalReviews }}次複習</p>
            <p class="text-primary mt-1">{{ card.nextReviewDate }}</p>
          </div>
        </div>
      </div>

      <div v-if="allCards.length === 0" class="text-center py-16 text-gray-500">
        <div class="text-4xl mb-4">🗂</div>
        <p>還沒有閃卡，點擊「生成閃卡」讓 AI 幫你創建</p>
      </div>
    </div>

    <!-- Generate Modal -->
    <div v-if="showGenerate" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div class="card w-full max-w-lg">
        <h3 class="font-semibold text-lg mb-4">AI 生成閃卡</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm text-gray-400 mb-1">學習內容</label>
            <textarea v-model="generateForm.content" class="input resize-none" rows="5"
              placeholder="貼上你的學習筆記、課文內容，AI 將自動提取知識點並生成閃卡..." />
          </div>
          <div>
            <label class="block text-sm text-gray-400 mb-1">生成數量</label>
            <select v-model.number="generateForm.count" class="input">
              <option :value="5">5 張</option>
              <option :value="10">10 張</option>
              <option :value="20">20 張</option>
            </select>
          </div>
        </div>
        <div class="flex gap-3 mt-6">
          <button @click="generateCards" class="btn-primary flex-1" :disabled="generating">
            {{ generating ? '生成中...' : 'AI 生成閃卡' }}
          </button>
          <button @click="showGenerate = false" class="btn-secondary">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { flashcardsApi, goalsApi } from '@/api'

const route = useRoute()
const allCards = ref([])
const dueCards = ref([])
const reviewMode = ref(false)
const reviewIdx = ref(0)
const showAnswer = ref(false)
const reviewedToday = ref(0)
const showGenerate = ref(false)
const generating = ref(false)
const topic = ref('')
const generateForm = ref({ content: '', count: 10 })

const currentCard = computed(() => dueCards.value[reviewIdx.value])

const ratings = [
  { value: 1, label: '完全不會', desc: '1天後', cls: 'bg-red-900/40 hover:bg-red-900/60 text-red-400' },
  { value: 2, label: '模糊', desc: '1天後', cls: 'bg-orange-900/40 hover:bg-orange-900/60 text-orange-400' },
  { value: 3, label: '記得', desc: '6天後', cls: 'bg-yellow-900/40 hover:bg-yellow-900/60 text-yellow-400' },
  { value: 5, label: '輕鬆', desc: '更長', cls: 'bg-green-900/40 hover:bg-green-900/60 text-green-400' },
]

onMounted(async () => {
  const g = await goalsApi.get(route.params.id)
  topic.value = g.topic
  await loadCards()
})

async function loadCards() {
  allCards.value = await flashcardsApi.getAll(route.params.id)
  dueCards.value = await flashcardsApi.getDue(route.params.id)
}

function startReview() {
  reviewMode.value = true
  reviewIdx.value = 0
  showAnswer.value = false
}

function exitReview() {
  reviewMode.value = false
  loadCards()
}

async function rateCard(rating) {
  await flashcardsApi.review(currentCard.value.id, rating)
  reviewedToday.value++
  showAnswer.value = false
  if (reviewIdx.value + 1 >= dueCards.value.length) {
    reviewMode.value = false
    loadCards()
  } else {
    reviewIdx.value++
  }
}

async function generateCards() {
  generating.value = true
  try {
    await flashcardsApi.generate({ goalId: route.params.id, ...generateForm.value })
    await loadCards()
    showGenerate.value = false
    generateForm.value.content = ''
  } finally {
    generating.value = false
  }
}
</script>
