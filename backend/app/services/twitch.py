import requests
from typing import List, Dict
from app.core.config import get_settings
from datetime import datetime, timedelta, timezone

settings = get_settings()

class TwitchService:
    def __init__(self):
        self.client_id = settings.twitch_client_id
        self.client_secret = settings.twitch_client_secret
        self.token_url = settings.twitch_token_url
        self.api_base_url = settings.twitch_api_url
        self.access_token = None
        self.token_expiry = None

    def get_access_token(self) -> str:

        if self.access_token and self.token_expiry and datetime.now(timezone.utc) < self.token_expiry:
            return self.access_token  # Reuse the token if it's still valid

        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        
        response = requests.post(self.token_url, data=payload)
        response.raise_for_status()
        token_data = response.json()
        self.access_token = token_data['access_token']
        expires_in = token_data.get('expires_in', 0)
        self.token_expiry = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        return self.access_token
    
    def autocomplete_games(self, query: str) -> List[Dict]:

        access_token = self.get_access_token()
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {access_token}'
        }
        url = f"{self.api_base_url}/search/categories"
        params = {'query': query}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get('data', [])

    def get_game_id(self, game_name: str) -> str:

        access_token = self.get_access_token()
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {access_token}'
        }
        url = f"{self.api_base_url}/games"
        params = {'name': game_name}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json().get('data', [])
        
        if not data:
            return None
        
        return data[0]['id']

    def get_videos_by_game_id(self, game_id: str) -> List[Dict]:

        access_token = self.get_access_token()
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {access_token}'
        }
        url = f"{self.api_base_url}/videos"
        params = {
            'game_id': game_id,
            'first': 10 
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get('data', [])

    def search_videos_by_game_name(self, game_name: str) -> List[Dict]:

        game_id = self.get_game_id(game_name)
        if not game_id:
            return []
        return self.get_videos_by_game_id(game_id)
    



