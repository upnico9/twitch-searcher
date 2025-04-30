
export interface Video {
    id: string
    stream_id: string
    user_id: string
    user_login: string
    user_name: string
    title: string
    description: string
    created_at: string
    published_at: string
    url: string
    thumbnail_url: string
    viewable: string
    view_count: number
    language: string
    type: string
    duration: string
    muted_segments: any
  }

  export interface Game {
    id: string
    name: string
  }
    
  export interface GameOption {
    label: string
    value: string
  }
  
  export interface SearchQuery {
    query: string
    language?: string
    sort?: string
    period?: string
  }
  