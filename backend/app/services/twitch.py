import requests
from typing import Optional, List, Dict
from datetime import datetime, timedelta, timezone
from app.core.config import get_settings
from app.core.errors.exceptions import ExternalServiceException

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
        try:
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
        except requests.RequestException as e:
            raise ExternalServiceException("Twitch Authentication", str(e))
    
    def autocomplete_games(self, query: str) -> List[Dict]:
        try:
            access_token = self.get_access_token()
            headers = {
                'Client-ID': self.client_id,
                'Authorization': f'Bearer {access_token}'
            }
            url = f"{self.api_base_url}/search/categories"
            params = {'query': query}

            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            results = response.json().get('data', [])
            return results
        except ExternalServiceException:
            # Re-raise already handled exceptions
            raise
        except requests.RequestException as e:
            raise ExternalServiceException("Twitch API", f"Game autocomplete failed: {str(e)}")

    def get_game_id(self, game_name: str) -> str:
        try:
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
            
            game_id = data[0]['id']
            return game_id
        except ExternalServiceException:
            # Re-raise already handled exceptions
            raise
        except requests.RequestException as e:
            raise ExternalServiceException("Twitch API", f"Game ID lookup failed: {str(e)}")

    def get_videos_by_game_id(
        self,
        game_id: str,
        language: Optional[str] = None,
        sort: Optional[str] = None,
        period: Optional[str] = None
    ) -> List[Dict]:
        try:
            access_token = self.get_access_token()
            headers = {
                'Client-ID': self.client_id,
                'Authorization': f'Bearer {access_token}'
            }

            url = f"{self.api_base_url}/videos"
            params = {
                'game_id': game_id,
                'first': 50,
            }

            if language:
                params['language'] = language
            if sort in ['time', 'trending', 'views']:
                params['sort'] = sort
            if period in ['all', 'day', 'week', 'month']:
                params['period'] = period

            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            videos = response.json().get('data', [])
            return videos
        except ExternalServiceException:
            # Re-raise already handled exceptions
            raise
        except requests.RequestException as e:
            raise ExternalServiceException("Twitch API", f"Video retrieval failed: {str(e)}")

    def search_videos_by_game_name(self, game_name: str) -> List[Dict]:
        try:
            game_id = self.get_game_id(game_name)
            if not game_id:
                return []
            videos = self.get_videos_by_game_id(game_id)
            return videos
        except ExternalServiceException:
            # Already handled by the methods above
            raise






