<template>
  <div class="p-8 max-w-4xl mx-auto">
    <div class="mb-6 flex items-center gap-3">
      <router-link :to="`/goals/${route.params.id}`" class="text-gray-500 hover:text-white">←</router-link>
      <h1 class="text-2xl font-bold">🎯 刻意練習</h1>
    </div>

    <!-- Config Panel (before starting) -->
    <div v-if="!session.active" class="card mb-6">
      <h2 class="font-semibold mb-4">配置練習</h2>
      <div class="grid grid-cols-2 gap-4 mb-4">
        <div>
          <label class="block text-sm text-gray-400 mb-1">子主題</label>
          <input v-model="config.subtopic" class="input" :placeholder="`例如：${topic} 中的某個具體概念`" />
        </div>
        <div>
          <label class="block text-sm text-gray-400 mb-1">難度</label>
          <select v-model="config.difficulty" class="input">
            <option value="easy">簡單</option>
            <option value="medium">中等</option>
            <option value="hard">困難</option>
          </select>
        </div>
        <div>
          <label class="block text-sm text-gray-400 mb-1">題型</label>
          <select v-model="config.question_type" class="input">
            <option value="multiple_choice">選擇題</option>
            <option value="short_answer">簡答題</option>
            <option value="problem_solving">解題</option>
          </select>
        </div>
        <div>
          <label class="block text-sm text-gray-400 mb-1">題目數量</label>
          <select v-model.number="config.count" class="input">
            <option :value="3">3 題</option>
            <option :value="5">5 題</option>
            <option :value="10">10 題</option>
          </select>
        </div>
      </div>
      <button @click="startSession" class="btn-primary w-full py-3" :disabled="loading">
        {{ loading ? '🤖 AI 生成題目中...' : '開始練習' }}
      </button>
    </div>

    <!-- Quiz -->
    <div v-if="session.active && !session.finished">
      <!-- Progress -->
      <div class="flex items-center gap-3 mb-6">
        <span class="text-sm text-gray-400">{{ session.currentIdx + 1 }} / {{ questions.length }}</span>
        <div class="flex-1 h-2 bg-surface-card rounded-full overflow-hidden">
          <div class="h-full bg-primary progress-bar rounded-full"
            :style="`width: ${((session.currentIdx) / questions.length) * 100}%`" />
        </div>
        <span class="text-sm text-green-400">✓ {{ session.correct }}</span>
        <span class="text-sm text-red-400">✗ {{ session.wrong }}</span>
      </div>

      <!-- Question Card -->
      <div class="card mb-4" v-if="currentQ">
        <div class="flex items-start gap-3 mb-4">
          <span class="badge bg-primary/20 text-primary text-xs">{{ diffLabel(currentQ.difficulty) }}</span>
          <span class="text-xs text-gray-500">{{ currentQ.key_concept }}</span>
        </div>
        <p class="text-lg font-medium mb-6">{{ currentQ.question }}</p>

        <!-- Multiple Choice -->
        <div v-if="currentQ.type === 'multiple_choice'" class="space-y-3">
          <button v-for="opt in currentQ.options" :key="opt"
            @click="selectOption(opt)"
            :disabled="answered"
            :class="optionClass(opt)"
            class="w-full text-left p-4 rounded-lg border transition-all duration-200">
            {{ opt }}
          </button>
        </div>

        <!-- Short Answer -->
        <div v-else>
          <textarea v-model="userAnswer" class="input resize-none" rows="4"
            placeholder="輸入你的答案..." :disabled="answered" />
          <button v-if="!answered" @click="submitAnswer"
            class="btn-primary mt-3" :disabled="!userAnswer.trim() || evaluating">
            {{ evaluating ? '評估中...' : '提交答案' }}
          </button>
        </div>
      </div>

      <!-- Feedback -->
      <div v-if="feedback" class="card mb-4"
        :class="feedback.is_correct ? 'border-green-500/50' : 'border-red-500/50'">
        <div class="flex items-center gap-2 mb-3">
          <span class="text-xl">{{ feedback.is_correct ? '✅' : '❌' }}</span>
          <span class="font-semibold" :class="feedback.is_correct ? 'text-green-400' : 'text-red-400'">
            {{ feedback.is_correct ? `正確！得分：${feedback.score}` : `錯誤。得分：${feedback.score}` }}
          </span>
        </div>
        <p class="text-gray-300 mb-3">{{ feedback.explanation }}</p>
        <div v-if="feedback.feedback?.corrections?.length" class="mb-3">
          <p class="text-sm font-medium text-yellow-400 mb-1">需要注意：</p>
          <ul class="text-sm text-gray-400 space-y-1">
            <li v-for="c in feedback.feedback.corrections" :key="c">• {{ c }}</li>
          </ul>
        </div>
        <p class="text-sm text-primary italic">{{ feedback.encouragement }}</p>
        <button @click="nextQuestion" class="btn-primary mt-4">
          {{ session.currentIdx + 1 < questions.length ? '下一題 →' : '查看結果' }}
        </button>
      </div>
    </div>

    <!-- Results -->
    <div v-if="session.finished" class="card text-center">
      <div class="text-6xl mb-4">{{ session.correct / questions.length >= 0.8 ? '🏆' : session.correct / questions.length >= 0.6 ? '📈' : '💪' }}</div>
      <h2 class="text-2xl font-bold mb-2">練習完成！</h2>
      <p class="text-gray-400 mb-6">正確率 {{ Math.round(session.correct / questions.length * 100) }}%</p>
      <div class="grid grid-cols-3 gap-4 mb-8">
        <div class="bg-surface rounded-lg p-4">
          <p class="text-2xl font-bold text-green-400">{{ session.correct }}</p>
          <p class="text-gray-400 text-sm">正確</p>
        </div>
        <div class="bg-surface rounded-lg p-4">
          <p class="text-2xl font-bold text-red-400">{{ session.wrong }}</p>
          <p class="text-gray-400 text-sm">錯誤</p>
        </div>
        <div class="bg-surface rounded-lg p-4">
          <p class="text-2xl font-bold text-primary">{{ questions.length }}</p>
          <p class="text-gray-400 text-sm">總題數</p>
        </div>
      </div>
      <div class="flex gap-3 justify-center">
        <button @click="resetSession" class="btn-primary">再練一次</button>
        <router-link :to="`/goals/${route.params.id}`" class="btn-secondary">返回目標</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { goalsApi, aiApi } from '@/api'

const route = useRoute()
const topic = ref('')
const loading = ref(false)
const evaluating = ref(false)
const questions = ref([])
const answered = ref(false)
const userAnswer = ref('')
const selectedOpt = ref(null)
const feedback = ref(null)

const config = ref({ subtopic: '', difficulty: 'medium', question_type: 'multiple_choice', count: 5 })
const session = ref({ active: false, finished: false, currentIdx: 0, correct: 0, wrong: 0 })

const currentQ = computed(() => questions.value[session.value.currentIdx] || null)

onMounted(async () => {
  const g = await goalsApi.get(route.params.id)
  topic.value = g.topic
  config.value.subtopic = g.topic
})

async function startSession() {
  loading.value = true
  try {
    const result = await aiApi.getDrillQuestions({ topic: topic.value, ...config.value })
    questions.value = result.questions || []
    session.value = { active: true, finished: false, currentIdx: 0, correct: 0, wrong: 0 }
    feedback.value = null
    answered.value = false
  } finally {
    loading.value = false
  }
}

function selectOption(opt) {
  if (answered.value) return
  selectedOpt.value = opt
  const q = currentQ.value
  const correct = opt.startsWith(q.correct_answer) || opt === q.correct_answer
  feedback.value = {
    is_correct: correct,
    score: correct ? 100 : 0,
    explanation: q.explanation,
    encouragement: correct ? '答得很好！' : '再仔細思考一下這個概念吧！',
    feedback: { corrections: correct ? [] : [`正確答案是：${q.correct_answer}`] }
  }
  if (correct) session.value.correct++
  else session.value.wrong++
  answered.value = true
}

async function submitAnswer() {
  evaluating.value = true
  try {
    const q = currentQ.value
    const result = await aiApi.evaluateAnswer({
      question: q.question, correct_answer: q.correct_answer,
      user_answer: userAnswer.value, topic: topic.value
    })
    feedback.value = result
    if (result.is_correct) session.value.correct++
    else session.value.wrong++
    answered.value = true
  } finally {
    evaluating.value = false
  }
}

function nextQuestion() {
  if (session.value.currentIdx + 1 >= questions.value.length) {
    session.value.finished = true
  } else {
    session.value.currentIdx++
    feedback.value = null
    answered.value = false
    userAnswer.value = ''
    selectedOpt.value = null
  }
}

function resetSession() {
  session.value = { active: false, finished: false, currentIdx: 0, correct: 0, wrong: 0 }
  questions.value = []
  feedback.value = null
}

function optionClass(opt) {
  if (!answered.value) return 'border-surface-border hover:border-primary text-gray-300'
  const q = currentQ.value
  const isCorrect = opt.startsWith(q.correct_answer) || opt === q.correct_answer
  const isSelected = opt === selectedOpt.value
  if (isCorrect) return 'border-green-500 bg-green-900/20 text-green-300'
  if (isSelected && !isCorrect) return 'border-red-500 bg-red-900/20 text-red-300'
  return 'border-surface-border text-gray-500'
}

function diffLabel(d) {
  return { easy: '簡單', medium: '中等', hard: '困難' }[d] || d
}
</script>
