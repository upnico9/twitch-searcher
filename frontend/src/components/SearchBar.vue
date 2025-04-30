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
  
          <n-button
            type="primary"
            class="search-button"
            @click="onSearch"
          >
            🔍 Rechercher
          </n-button>
        </div>
      </n-spin>
    </n-card>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import { useMessage } from 'naive-ui'
  import { autocompleteGames, searchGames } from '../api/api'
  import type { GameOption, Video, Game } from '../types'

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
      console.log("Selected game ID:", selectedGameId.value)
      console.log("Selected game name:", selected.label)
    } else {
        console.log("Aucun jeu sélectionné, je suis pas censé aller la")
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
    const result = await searchGames({
      game_id: selectedGameId.value,
      language: selectedLanguage.value ?? undefined,
      sort: selectedSort.value ?? undefined,
      period: selectedPeriod.value ?? undefined
    })

    emit('update:videos', result.videos)
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
  
  .search-button {
    flex: 1;
    min-width: 180px;
    font-weight: bold;
    background-color: #9147ff;
    border: none;
  }
  </style>
  