<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-2xl mb-4">
          <span class="text-3xl">⚡</span>
        </div>
        <h1 class="text-3xl font-bold text-white">Ultralearning AI</h1>
        <p class="text-gray-400 mt-2">開始你的超級學習之旅</p>
      </div>

      <div class="card">
        <h2 class="text-xl font-semibold mb-6">創建帳戶</h2>
        <form @submit.prevent="handleRegister" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm text-gray-400 mb-1">用戶名 *</label>
              <input v-model="form.username" class="input" placeholder="user123" required />
            </div>
            <div>
              <label class="block text-sm text-gray-400 mb-1">顯示名稱</label>
              <input v-model="form.displayName" class="input" placeholder="你的名字" />
            </div>
          </div>
          <div>
            <label class="block text-sm text-gray-400 mb-1">郵箱 *</label>
            <input v-model="form.email" type="email" class="input" placeholder="you@example.com" required />
          </div>
          <div>
            <label class="block text-sm text-gray-400 mb-1">密碼 *</label>
            <input v-model="form.password" type="password" class="input" placeholder="至少6個字符" required />
          </div>
          <div>
            <label class="block text-sm text-gray-400 mb-1">你的背景/興趣（幫助 AI 個性化學習）</label>
            <textarea v-model="form.learnerBackground" class="input resize-none" rows="2"
              placeholder="例如：軟體工程師，喜歡科幻小說，有10年程式設計經驗..." />
          </div>
          <div v-if="error" class="text-red-400 text-sm bg-red-900/20 rounded-lg p-3">{{ error }}</div>
          <button type="submit" class="btn-primary w-full py-3" :disabled="loading">
            {{ loading ? '創建中...' : '創建帳戶' }}
          </button>
        </form>
        <p class="mt-4 text-center text-gray-400 text-sm">
          已有帳戶？
          <router-link to="/login" class="text-primary hover:underline">登入</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const auth = useAuthStore()
const router = useRouter()
const form = ref({ username: '', email: '', password: '', displayName: '', learnerBackground: '' })
const loading = ref(false)
const error = ref('')

async function handleRegister() {
  loading.value = true
  error.value = ''
  try {
    await auth.register(form.value)
    router.push('/dashboard')
  } catch (e) {
    error.value = e?.error || '註冊失敗，請重試'
  } finally {
    loading.value = false
  }
}
</script>
