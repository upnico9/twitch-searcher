from fastapi import FastAPI
from app.core.config import get_settings
from app.services.twitch import TwitchService

app = FastAPI(
        title="Twitch Video Searcher",
        description="Simple API to search Twitch videos by game name",
        version="0.1.0",
    )

# settings = get_settings()
# twitch_service = TwitchService()

# token = twitch_service.get_access_token()


# games = twitch_service.autocomplete_games("fifa")
# print(games)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}