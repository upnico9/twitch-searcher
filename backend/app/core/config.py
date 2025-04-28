from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Twitch credentials
    twitch_client_id: str
    twitch_client_secret: str
    twitch_token_url: str = "https://id.twitch.tv/oauth2/token"
    twitch_api_url: str = "https://api.twitch.tv/helix"

    # Mongo settings
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "twitch_search_db"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
