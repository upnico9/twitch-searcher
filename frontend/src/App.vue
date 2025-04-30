<template>
  <n-config-provider :theme="theme" :theme-overrides="themeOverrides">
    <n-message-provider>
      <div class="app-container">
        
        <n-card class="title-card" size="large" bordered>
          <h1 class="app-title">🎯 Twitch <span class="highlight">Researcher</span></h1>
          <p class="app-subtitle">Recuperer tes clips twitch préférés</p>
        </n-card>

        <SearchBar @update:videos="handleUpdateVideos" />

        <VideoPlayer
          v-if="selectedVideo"
          :video="selectedVideo"
          @close="selectedVideo = null"
        />
        <VideoList
          v-if="videos.length"
          :videos="videos"
          @selectVideo="selectedVideo = $event"
        />

        <div v-else class="empty-state">
          🔎 Aucune vidéo trouvée.
        </div>
      </div>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import SearchBar from './components/SearchBar.vue'
import VideoList from './components/VideoList.vue'
import VideoPlayer from './components/VideoPlayer.vue'
import { theme, themeOverrides } from './naive-themes'
import type { Video } from './types'

const videos = ref<Video[]>([])
const selectedVideo = ref<Video | null>(null)

const handleUpdateVideos = (newVideos: Video[]) => {
  videos.value = newVideos
  selectedVideo.value = null
}
</script>

<style scoped>
.app-container {
  background: linear-gradient(135deg, #0e0e10 0%, #1f1f23 100%);
  min-height: 100vh;
  padding: 2rem;
  color: white;
}

.title-card {
  background-color: #262626;
  color: white;
  text-align: center;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
  max-width: 700px;
  margin: 0 auto 2rem;
}

.app-title {
  font-size: 3rem;
  font-weight: 800;
  margin: 0;
}

.highlight {
  color: #9147ff;
}

.app-subtitle {
  font-size: 1.1rem;
  margin-top: 1rem;
  color: #c0c0c0;
}

.empty-state {
  text-align: center;
  margin-top: 4rem;
  font-size: 1.2rem;
  color: #888;
}
</style>
