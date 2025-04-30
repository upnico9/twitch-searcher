<template>
  <n-card class="search-bar" bordered>
    <n-spin :show="isLoading">
      <div class="filters">
        <n-auto-complete
          v-model:value="searchTerm"
          :options="gameOptions"
          placeholder="Rechercher un jeu..."
          clearable
          class="input"
          @update:value="handleInput"
          @select="handleSelect"
        />

        <n-select
          v-model:value="selectedLanguage"
          :options="languageOptions"
          placeholder="Langue"
          class="select"
        />

        <n-select
          v-model:value="selectedSort"
          :options="sortOptions"
          placeholder="Trier par"
          class="select"
        />

        <n-select
          v-model:value="selectedPeriod"
          :options="periodOptions"
          placeholder="Période"
          class="select"
        />

        <div class="action-buttons">
          <n-button
            type="primary"
            class="search-button"
            @click="onSearch"
          >
            🔍 Rechercher
          </n-button>
          
          <n-tooltip placement="bottom">
            <template #trigger>
              <n-button
                :type="isAutoRefreshActive ? 'warning' : 'default'"
                class="refresh-button"
                @click="toggleAutoRefresh"
                :ghost="!isAutoRefreshActive"
              >
                <template #icon>
                  <n-icon><refresh-icon /></n-icon>
                </template>
                {{ isAutoRefreshActive ? 'Arrêter' : 'Auto' }}
              </n-button>
            </template>
            {{ isAutoRefreshActive ? 'Désactiver l\'actualisation automatique' : 'Activer l\'actualisation automatique (2min)' }}
          </n-tooltip>
        </div>
      </div>

      <div v-if="isAutoRefreshActive" class="auto-refresh-indicator">
        <n-space align="center">
          <n-icon color="#9147ff" size="16" class="rotating-icon"><refresh-icon /></n-icon>
          <span>Actualisation auto activée</span>
        </n-space>
      </div>
    </n-spin>
  </n-card>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from 'vue'
import { useMessage } from 'naive-ui'
import { autocompleteGames, searchGames } from '../api/api'
import type { GameOption, Video, Game } from '../types'
import { RefreshOutline as RefreshIcon } from '@vicons/ionicons5'

const emit = defineEmits<{
  (e: 'update:videos', videos: Video[]): void
}>()

const gameOptions = ref<GameOption[]>([])

const message = useMessage()
const isLoading = ref(false)

const searchTerm = ref('')
const selectedGameId = ref<string | null>(null)

const selectedLanguage = ref<string | null>(null)
const selectedSort = ref<string | null>(null)
const selectedPeriod = ref<string | null>(null)

let debounceTimeout: ReturnType<typeof setTimeout> | null = null

const languageOptions = [
  { label: 'Français', value: 'fr' },
  { label: 'English', value: 'en' },
  { label: 'Español', value: 'es' },
  { label: 'Deutsch', value: 'de' },
  { label: 'Português', value: 'pt' },
  { label: '日本語', value: 'ja' }
]

const sortOptions = [
  { label: 'Temps', value: 'time' },
  { label: 'Tendance', value: 'trending' },
  { label: 'Vues', value: 'views' }
]

const periodOptions = [
  { label: 'Tout', value: 'all' },
  { label: 'Jour', value: 'day' },
  { label: 'Semaine', value: 'week' },
  { label: 'Mois', value: 'month' }
]

const isAutoRefreshActive = ref(false)
let autoRefreshInterval: ReturnType<typeof setInterval> | null = null
let lastSearchParams: any = null

const startAutoRefresh = () => {
  stopAutoRefresh()

  lastSearchParams = {
    game_id: selectedGameId.value,
    language: selectedLanguage.value ?? undefined,
    sort: selectedSort.value ?? undefined,
    period: selectedPeriod.value ?? undefined
  }

  autoRefreshInterval = setInterval(async () => {
    try {
      const result = await searchGames(lastSearchParams)
      emit('update:videos', result.videos)
      
      message.success('Résultats actualisés', { duration: 1500 })
    } catch (error) {
      console.error('Erreur lors de l\'actualisation automatique:', error)
      message.error('L\'actualisation automatique a échoué', { duration: 3000 })
    }
  }, 120000) // 2 minutes
  
  isAutoRefreshActive.value = true
}

const stopAutoRefresh = () => {
  if (autoRefreshInterval !== null) {
    clearInterval(autoRefreshInterval)
    autoRefreshInterval = null
    isAutoRefreshActive.value = false
  }
}

const toggleAutoRefresh = () => {
  if (isAutoRefreshActive.value) {
    stopAutoRefresh()
    message.info('Actualisation automatique désactivée')
  } else {
    if (!selectedGameId.value) {
      message.warning('Veuillez d\'abord effectuer une recherche')
      return
    }
    startAutoRefresh()
    message.success('Actualisation automatique activée (toutes les 2 minutes)')
  }
}

onUnmounted(() => {
  stopAutoRefresh()
  if (debounceTimeout) clearTimeout(debounceTimeout)
})

const handleInput = (value: string) => {
  if (debounceTimeout) clearTimeout(debounceTimeout)

  if (value.length < 3) {
    gameOptions.value = []
    return
  }

  debounceTimeout = setTimeout(async () => {
    try {
      const response = await autocompleteGames(value)
      const games = response.games

      gameOptions.value = (games as Game[]).map((game) => ({
        label: game.name,
        value: game.id
      }))
    } catch (error) {
      console.error("Erreur lors de l'autocomplete:", error)
    }
  }, 300)
}


const handleSelect = (value: string) => {
  const selected = gameOptions.value.find((opt: { value: string; label: string }) => opt.value === value)
  if (selected) {
    selectedGameId.value = selected.value
    searchTerm.value = selected.label
  } else {
    selectedGameId.value = null
  }
}

const onSearch = async () => {
  if (!selectedGameId.value || !gameOptions.value.find(opt => opt.value === selectedGameId.value)) {
    message.error('Veuillez sélectionner un jeu dans la liste proposée.')
    return
  }

  isLoading.value = true

  try {
    const searchParams = {
      game_id: selectedGameId.value,
      language: selectedLanguage.value ?? undefined,
      sort: selectedSort.value ?? undefined,
      period: selectedPeriod.value ?? undefined
    }
    
    const result = await searchGames(searchParams)
    emit('update:videos', result.videos)
    
    lastSearchParams = searchParams
  } catch (error) {
    console.error('Erreur lors de la recherche:', error)
    message.error('Erreur lors de la recherche. Veuillez réessayer.')
  } finally {
    isLoading.value = false
  }
}

</script>

<style scoped>
.search-bar {
  background-color: #262626;
  color: white;
  margin: 2rem auto;
  max-width: 900px;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 1.2rem;
  align-items: center;
  justify-content: center;
}

.input {
  flex: 2;
  min-width: 250px;
}

.select {
  flex: 1;
  min-width: 180px;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  flex: 1;
  min-width: 180px;
}

.search-button {
  flex-grow: 1;
  font-weight: bold;
  background-color: #9147ff;
  border: none;
}

.refresh-button {
  min-width: 80px;
}

.auto-refresh-indicator {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  font-size: 0.9rem;
  color: #9147ff;
}

.rotating-icon {
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>