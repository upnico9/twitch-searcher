from fastapi import APIRouter, Query, HTTPException
from app.services.twitch import TwitchService

router = APIRouter()
twitch_service = TwitchService()

@router.get("/autocomplete")
def autocomplete_games(game: str = Query(..., description="Partial name to autocomplete games")):
    games = twitch_service.autocomplete_games(game)
    if not games:
        raise HTTPException(status_code=404, detail="No games matching this query")
    return {"games": games}
