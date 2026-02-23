<template>
  <div class="flex h-screen overflow-hidden">
    <!-- Sidebar -->
    <aside class="w-64 bg-surface-card border-r border-surface-border flex flex-col shrink-0">
      <!-- Logo -->
      <div class="p-6 border-b border-surface-border">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 bg-primary rounded-lg flex items-center justify-center text-xl">⚡</div>
          <div>
            <p class="font-bold text-white text-sm">Ultralearning</p>
            <p class="text-xs text-gray-500">AI 超級學習</p>
          </div>
        </div>
      </div>

      <!-- Nav -->
      <nav class="flex-1 p-4 space-y-1">
        <router-link to="/dashboard" class="nav-link" active-class="nav-link-active">
          <span>📊</span> 儀表板
        </router-link>
        <router-link to="/goals/new" class="nav-link" active-class="nav-link-active">
          <span>➕</span> 新增學習目標
        </router-link>

        <!-- Goals List -->
        <div class="mt-4 pt-4 border-t border-surface-border">
          <p class="text-xs text-gray-500 uppercase tracking-wider mb-2 px-3">我的學習目標</p>
          <div v-for="goal in goals.goals" :key="goal.id" class="mb-1">
            <router-link :to="`/goals/${goal.id}`" class="nav-link text-sm" active-class="nav-link-active">
              <span>📚</span>
              <span class="truncate">{{ goal.topic }}</span>
              <span class="ml-auto text-xs text-gray-500">{{ goal.overallProgress }}%</span>
            </router-link>
          </div>
        </div>
      </nav>

      <!-- User -->
      <div class="p-4 border-t border-surface-border">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-sm font-bold">
            {{ auth.user?.displayName?.[0]?.toUpperCase() || 'U' }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate">{{ auth.user?.displayName }}</p>
            <p class="text-xs text-gray-500 truncate">{{ auth.user?.email }}</p>
          </div>
          <button @click="handleLogout" class="text-gray-500 hover:text-white transition-colors text-lg">⏏</button>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-auto">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useGoalsStore } from '@/store/goals'

const auth = useAuthStore()
const goals = useGoalsStore()
const router = useRouter()

onMounted(() => goals.fetchGoals())

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.nav-link {
  @apply flex items-center gap-3 px-3 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-surface transition-colors duration-150 cursor-pointer no-underline;
}
.nav-link-active {
  @apply bg-primary/20 text-primary;
}
</style>
