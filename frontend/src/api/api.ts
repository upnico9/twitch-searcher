import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000', 
  timeout: 5000
})


export const autocompleteGames = async (game: string) => {
  const response = await api.get('/api/autocomplete', {
    params: { game }
  })
  return response.data
}

export const searchGames = async (params: {
  game_id: string
  language?: string
  sort?: string
  period?: string
}) => {
  const response = await api.get('/api/search', {
    params
  })
  return response.data
}
