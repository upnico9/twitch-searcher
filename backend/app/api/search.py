from fastapi import APIRouter, Query, HTTPException
from app.services.twitch import TwitchService

router = APIRouter()
twitch_service = TwitchService()

@router.get("/search")
def search_videos(game_id: str = Query(..., description="Game name to search videos for")):
    videos = twitch_service.get_videos_by_game_id(game_id)
    if not videos:
        raise HTTPException(status_code=404, detail="No videos found for this game")
    return {"videos": videos}
