<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-2xl mb-4">
          <span class="text-3xl">⚡</span>
        </div>
        <h1 class="text-3xl font-bold text-white">Ultralearning AI</h1>
        <p class="text-gray-400 mt-2">AI 驅動的超級學習系統</p>
      </div>

      <div class="card">
        <h2 class="text-xl font-semibold mb-6">登入帳戶</h2>
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm text-gray-400 mb-1">用戶名</label>
            <input v-model="form.username" type="text" class="input" placeholder="輸入用戶名" required />
          </div>
          <div>
            <label class="block text-sm text-gray-400 mb-1">密碼</label>
            <input v-model="form.password" type="password" class="input" placeholder="輸入密碼" required />
          </div>
          <div v-if="error" class="text-red-400 text-sm bg-red-900/20 rounded-lg p-3">{{ error }}</div>
          <button type="submit" class="btn-primary w-full py-3" :disabled="loading">
            {{ loading ? '登入中...' : '登入' }}
          </button>
        </form>
        <p class="mt-4 text-center text-gray-400 text-sm">
          沒有帳戶？
          <router-link to="/register" class="text-primary hover:underline">立即註冊</router-link>
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
const form = ref({ username: '', password: '' })
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await auth.login(form.value)
    router.push('/dashboard')
  } catch (e) {
    error.value = e?.error || '登入失敗，請重試'
  } finally {
    loading.value = false
  }
}
</script>
