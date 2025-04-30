from fastapi import APIRouter, Query
from app.services.twitch import TwitchService
from app.core.errors.exceptions import ResourceNotFoundException

router = APIRouter()
twitch_service = TwitchService()

@router.get("/autocomplete")
def autocomplete_games(game: str = Query(..., description="Partial name to autocomplete games")):
    games = twitch_service.autocomplete_games(game)
    
    if not games:
        raise ResourceNotFoundException("Games", f"matching query: {game}")
    
    return {"games": games}
