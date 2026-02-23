<template>
  <div class="flex h-screen overflow-hidden">
    <!-- Sidebar -->
    <aside class="w-64 bg-surface-card border-r border-surface-border flex flex-col shrink-0">
      <!-- Logo -->
      <div class="p-5 border-b border-surface-border">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 bg-primary rounded-lg flex items-center justify-center text-xl shadow-lg shadow-primary/30">⚡</div>
          <div>
            <p class="font-bold text-white text-sm">Ultralearning</p>
            <p class="text-xs text-gray-500">AI 超級學習</p>
          </div>
        </div>
      </div>

      <!-- Nav -->
      <nav class="flex-1 p-3 space-y-0.5 overflow-y-auto">
        <router-link to="/dashboard" class="nav-link" active-class="nav-link-active">
          <span>📊</span>
          <span>儀表板</span>
        </router-link>
        <router-link to="/goals/new" class="nav-link" active-class="nav-link-active">
          <span>➕</span>
          <span>新增學習目標</span>
        </router-link>

        <!-- Goals List -->
        <div class="mt-4 pt-3 border-t border-surface-border">
          <p class="text-xs text-gray-500 uppercase tracking-wider mb-2 px-3">我的學習目標</p>
          <transition-group name="slide-up" tag="div">
            <div v-for="goal in goals.goals" :key="goal.id" class="mb-0.5">
              <router-link :to="`/goals/${goal.id}`" class="nav-link text-sm" active-class="nav-link-active">
                <span class="text-base">📚</span>
                <span class="truncate flex-1">{{ goal.topic }}</span>
                <span class="ml-auto text-xs shrink-0"
                      :class="goal.overallProgress >= 75 ? 'text-green-400' : goal.overallProgress >= 40 ? 'text-primary' : 'text-yellow-400'">
                  {{ goal.overallProgress }}%
                </span>
              </router-link>

              <!-- Flashcard due sub-links -->
              <div v-if="dueMap[goal.id]" class="ml-7 mt-0.5 mb-1">
                <router-link :to="`/goals/${goal.id}/flashcards`"
                  class="flex items-center gap-1.5 text-xs text-yellow-400 hover:text-yellow-300 transition-colors py-0.5">
                  <span class="w-1.5 h-1.5 rounded-full bg-yellow-400 badge-pulse inline-block"></span>
                  {{ dueMap[goal.id] }} 張閃卡待複習
                </router-link>
              </div>
            </div>
          </transition-group>
        </div>
      </nav>

      <!-- User -->
      <div class="p-4 border-t border-surface-border">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-gradient-to-br from-primary to-purple-500 rounded-full flex items-center justify-center text-sm font-bold shadow">
            {{ auth.user?.displayName?.[0]?.toUpperCase() || 'U' }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate">{{ auth.user?.displayName }}</p>
            <p class="text-xs text-gray-500 truncate">{{ auth.user?.email }}</p>
          </div>
          <button @click="handleLogout" title="登出"
            class="text-gray-500 hover:text-red-400 transition-colors text-lg p-1 rounded hover:bg-red-900/20">
            ⏏
          </button>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-auto">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useGoalsStore } from '@/store/goals'
import { flashcardsApi } from '@/api'

const auth = useAuthStore()
const goals = useGoalsStore()
const router = useRouter()
const dueMap = ref({})

onMounted(async () => {
  await goals.fetchGoals()
  loadDueCounts()
})

async function loadDueCounts() {
  for (const goal of goals.goals) {
    try {
      const res = await flashcardsApi.getDueCount(goal.id)
      if (res?.count > 0) dueMap.value[goal.id] = res.count
    } catch {}
  }
}

watch(() => goals.goals.length, loadDueCounts)

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.nav-link {
  @apply flex items-center gap-3 px-3 py-2 rounded-lg text-gray-400 hover:text-white hover:bg-surface transition-all duration-150 cursor-pointer no-underline text-sm;
}
.nav-link-active {
  @apply bg-primary/15 text-primary;
}
</style>
