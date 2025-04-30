<template>
    <n-card class="video-player" v-if="video">
      <div class="video-header">
        <h2 class="video-title">{{ video.title }}</h2>
        <n-button
          size="small"
          text
          class="close-button"
          @click="emit('close')"
        >
          ❌ Fermer
        </n-button>
      </div>
  
      <iframe
        class="video-iframe"
        :src="`https://player.twitch.tv/?video=${video.id}&parent=localhost`"
        width="100%"
        height="480"
        allowfullscreen
      />
      <div class="video-details">
        <p class="video-user">👤 {{ video.user_name }}</p>
        <p class="video-meta">
          🕒 {{ formatDuration(video.duration) }} |
          📅 {{ formatDate(video.created_at) }} |
          👁️ {{ video.view_count }} vues
        </p>
      </div>
    </n-card>
  </template>
  
  <script setup lang="ts">
  import { defineProps, defineEmits } from 'vue'
  import type { Video } from '../types'

  const props = defineProps<{
    video: Video
  }>()

  const emit = defineEmits<{
    (e: 'close'): void
  }>()

  const formatDuration = (d: string) => d || 'Durée inconnue'
  const formatDate = (d: string) =>
    new Date(d).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  </script>
  
  <style scoped>
  .video-player {
    background-color: #262626;
    color: white;
    max-width: 960px;
    margin: 2rem auto;
    padding: 1rem;
    border-radius: 1rem;
    box-shadow: 0 0 25px rgba(0, 0, 0, 0.4);
  }
  
  .video-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .video-iframe {
    border: none;
    border-radius: 0.5rem;
    margin: 1rem 0;
  }
  
  .video-details {
    text-align: left;
  }
  
  .video-title {
    font-size: 1.4rem;
    font-weight: bold;
    color: #9147ff;
    margin: 0;
  }
  
  .video-user,
  .video-meta {
    font-size: 1rem;
    color: #ccc;
    margin: 0.2rem 0;
  }
  
  .close-button {
    color: #aaa;
  }
  </style>
  