<template>
  <div class="p-8 max-w-4xl mx-auto">
    <div class="mb-6 flex items-center gap-3">
      <router-link :to="`/goals/${route.params.id}`" class="text-gray-500 hover:text-white">←</router-link>
      <h1 class="text-2xl font-bold">💡 費曼技巧 &amp; 直覺培養</h1>
    </div>

    <!-- Mode Tabs -->
    <div class="flex gap-2 mb-6">
      <button v-for="m in modes" :key="m.key"
        @click="activeMode = m.key"
        :class="activeMode === m.key ? 'bg-primary text-white' : 'bg-surface-card text-gray-400 hover:text-white'"
        class="px-4 py-2 rounded-lg text-sm font-medium transition-colors">
        {{ m.label }}
      </button>
    </div>

    <!-- ── Feynman Explain Mode ──────────────────────────── -->
    <div v-if="activeMode === 'explain'">
      <div class="card mb-4">
        <h2 class="font-semibold mb-4">請 AI 用費曼技巧解釋概念</h2>
        <div class="flex gap-3">
          <input v-model="concept" class="input flex-1" :placeholder="`輸入 ${topic} 中的一個概念...`" />
          <button @click="fetchExplanation" class="btn-primary whitespace-nowrap" :disabled="loading">
            {{ loading ? '分析中...' : '費曼解釋' }}
          </button>
        </div>
      </div>

      <div v-if="explanation" class="space-y-4">
        <!-- Core Essence -->
        <div class="card border-primary/30">
          <p class="text-xs text-gray-500 uppercase tracking-wider mb-2">本質</p>
          <p class="text-lg font-medium text-primary">{{ explanation.core_essence }}</p>
        </div>

        <!-- Simple Explanation -->
        <div class="card">
          <p class="text-xs text-gray-500 uppercase tracking-wider mb-3">簡單解釋（如同對孩子解釋）</p>
          <p class="text-gray-300 leading-relaxed">{{ explanation.simple_explanation }}</p>
        </div>

        <!-- Analogies -->
        <div class="card" v-if="explanation.analogies?.length">
          <p class="text-xs text-gray-500 uppercase tracking-wider mb-3">類比</p>
          <div v-for="a in explanation.analogies" :key="a.analogy" class="mb-4 last:mb-0 p-4 bg-surface rounded-lg">
            <p class="font-medium text-yellow-300">{{ a.analogy }}</p>
            <p class="text-sm text-green-400 mt-1">✓ 相似之處：{{ a.similarity }}</p>
            <p class="text-sm text-red-400 mt-0.5">✗ 不同之處：{{ a.difference }}</p>
          </div>
        </div>

        <!-- Examples + Why it matters -->
        <div class="grid grid-cols-2 gap-4">
          <div class="card" v-if="explanation.real_world_examples?.length">
            <p class="text-xs text-gray-500 uppercase tracking-wider mb-3">實際例子</p>
            <ul class="space-y-2">
              <li v-for="ex in explanation.real_world_examples" :key="ex" class="flex gap-2 text-sm text-gray-300">
                <span class="text-primary shrink-0">▸</span>{{ ex }}
              </li>
            </ul>
          </div>
          <div class="card">
            <p class="text-xs text-gray-500 uppercase tracking-wider mb-3">為什麼重要</p>
            <p class="text-sm text-gray-300">{{ explanation.why_it_matters }}</p>
          </div>
        </div>

        <!-- Deeper Questions -->
        <div class="card" v-if="explanation.deeper_questions?.length">
          <p class="text-xs text-gray-500 uppercase tracking-wider mb-3">深入思考的問題</p>
          <ul class="space-y-2">
            <li v-for="q in explanation.deeper_questions" :key="q"
              class="p-3 bg-surface rounded-lg text-sm text-gray-300 flex gap-2">
              <span class="text-primary">?</span>{{ q }}
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- ── Feynman Teach Mode ────────────────────────────── -->
    <div v-if="activeMode === 'teach'">
      <div class="card mb-4">
        <h2 class="font-semibold mb-2">用自己的話解釋，AI 給出反饋</h2>
        <p class="text-gray-400 text-sm mb-4">嘗試用最簡單的語言解釋一個概念，AI 將幫助你發現理解的盲點。</p>
        <div class="flex gap-3 mb-3">
          <input v-model="teachConcept" class="input flex-1" placeholder="要解釋的概念..." />
        </div>
        <textarea v-model="userExplanation" class="input resize-none w-full" rows="5"
          placeholder="用你自己的話解釋這個概念，假設你在向一個完全不懂的人解釋..." />
        <button @click="submitTeaching" class="btn-primary mt-3" :disabled="teachLoading || !userExplanation.trim()">
          {{ teachLoading ? '分析中...' : '提交解釋，獲取反饋' }}
        </button>
      </div>

      <div v-if="teachFeedback" class="card">
        <h3 class="font-semibold mb-3 text-primary flex items-center gap-2">
          <span>🤖</span> AI 導師反饋
          <span v-if="teachLoading" class="cursor-blink text-primary text-sm font-normal"></span>
        </h3>
        <div class="markdown-body" v-html="parsedTeachFeedback"></div>
      </div>
    </div>

    <!-- ── Analogies Mode ───────────────────────────────── -->
    <div v-if="activeMode === 'analogies'">
      <div class="card mb-4">
        <h2 class="font-semibold mb-4">個性化類比生成</h2>
        <div class="grid grid-cols-2 gap-3 mb-3">
          <input v-model="analogyConcept" class="input" placeholder="概念名稱..." />
          <input v-model="background" class="input" placeholder="你的背景/興趣（例如：籃球愛好者）" />
        </div>
        <button @click="fetchAnalogies" class="btn-primary" :disabled="analogyLoading">
          {{ analogyLoading ? '生成中...' : '生成個性化類比' }}
        </button>
      </div>

      <div v-if="analogies" class="space-y-4">
        <div v-for="a in analogies.personalized_analogies" :key="a.domain" class="card">
          <p class="text-xs text-gray-500 uppercase tracking-wider mb-2">{{ a.domain }}</p>
          <p class="text-gray-300 mb-4">{{ a.analogy }}</p>
          <div class="grid grid-cols-2 gap-3 mb-3">
            <div v-for="(val, key) in a.mapping" :key="key"
              class="flex items-center gap-2 text-sm bg-surface rounded-lg p-2">
              <span class="text-primary font-mono">{{ key }}</span>
              <span class="text-gray-500">→</span>
              <span class="text-yellow-300">{{ val }}</span>
            </div>
          </div>
          <p class="text-xs text-gray-500">⚠️ 局限：{{ a.limitations }}</p>
        </div>

        <div class="card" v-if="analogies.story">
          <p class="text-xs text-gray-500 uppercase tracking-wider mb-3">故事版本</p>
          <p class="text-gray-300 leading-relaxed italic">{{ analogies.story }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { goalsApi, aiApi } from '@/api'
import { marked } from 'marked'

const route = useRoute()
const topic = ref('')
const activeMode = ref('explain')
const loading = ref(false)
const concept = ref('')
const explanation = ref(null)
const teachConcept = ref('')
const userExplanation = ref('')
const teachLoading = ref(false)
const teachFeedback = ref('')
const analogyConcept = ref('')
const background = ref('')
const analogyLoading = ref(false)
const analogies = ref(null)

const parsedTeachFeedback = computed(() => marked.parse(teachFeedback.value || ''))

const modes = [
  { key: 'explain', label: '💡 費曼解釋' },
  { key: 'teach', label: '🎤 我來解釋' },
  { key: 'analogies', label: '🔗 個性化類比' },
]

onMounted(async () => {
  const g = await goalsApi.get(route.params.id)
  topic.value = g.topic
})

async function fetchExplanation() {
  if (!concept.value.trim()) return
  loading.value = true
  explanation.value = null
  try {
    explanation.value = await aiApi.feynmanExplain({ concept: concept.value, topic: topic.value })
  } finally {
    loading.value = false
  }
}

async function submitTeaching() {
  if (!userExplanation.value.trim()) return
  teachLoading.value = true
  teachFeedback.value = ''
  try {
    // Use streaming fetch
    const token = localStorage.getItem('token')
    const res = await fetch('/api/intuition/feynman-teach', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ concept: teachConcept.value || topic.value, user_explanation: userExplanation.value })
    })
    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      teachFeedback.value += decoder.decode(value)
    }
  } finally {
    teachLoading.value = false
  }
}

async function fetchAnalogies() {
  analogyLoading.value = true
  analogies.value = null
  try {
    analogies.value = await aiApi.getAnalogies({ concept: analogyConcept.value || topic.value, learner_background: background.value })
  } finally {
    analogyLoading.value = false
  }
}
</script>
