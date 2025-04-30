<template>
    <div class="video-list">
      <n-card
        v-for="video in videos"
        :key="video.id"
        class="video-card"
        hoverable
        @click="emit('selectVideo', video)"
      >
        <img
          :src="getThumbnail(video.thumbnail_url)"
          alt="Thumbnail"
          class="video-thumbnail"
        />
        <div class="video-info">
          <h3 class="video-title">{{ video.title }}</h3>
          <p class="video-user">👤 {{ video.user_name }}</p>
          <p class="video-meta">
            🕒 {{ formatDuration(video.duration) }} |
            {{ formatDate(video.created_at) }}
          </p>
          <p class="video-views">👁️ {{ video.view_count }} vues</p>
        </div>
      </n-card>
    </div>
  </template>
  
  <script setup lang="ts">
  import { defineEmits } from 'vue'
  import type { Video } from '../types'

  const props = defineProps<{
    videos: Video[]
  }>()

  const emit = defineEmits<{
    (e: 'selectVideo', video: Video): void
  }>()

  const getThumbnail = (url: string) =>
    url.replace('%{width}', '320').replace('%{height}', '180')
  
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
  .video-list {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    justify-content: center;
    margin-top: 2rem;
  }
  
  .video-card {
    background-color: #262626;
    color: white;
    width: 320px;
    padding: 1rem;
    border-radius: 1rem;
    text-align: center;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.4);
    transition: transform 0.2s;
    cursor: pointer;
  }
  
  .video-card:hover {
    transform: translateY(-5px);
  }
  
  .video-thumbnail {
    width: 100%;
    height: auto;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
  }
  
  .video-info {
    text-align: left;
  }
  
  .video-title {
    font-size: 1.1rem;
    font-weight: bold;
    color: #9147ff;
    margin-bottom: 0.5rem;
  }
  
  .video-user,
  .video-meta,
  .video-views {
    font-size: 0.9rem;
    margin: 0.2rem 0;
    color: #ccc;
  }
  </style>
  