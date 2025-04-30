from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from app.services.twitch import TwitchService

router = APIRouter()
twitch_service = TwitchService()

@router.get("/search")
def search_videos(
    game_id: str = Query(..., description="Game ID to search videos for"),
    language: Optional[str] = Query(None, description="Filter by language (e.g. 'en', 'fr')"),
    sort: Optional[str] = Query(None, description="Sort by 'time', 'trending' or 'views'"),
    period: Optional[str] = Query(None, description="Filter by 'day', 'week', 'month', or 'all'")
):
    videos = twitch_service.get_videos_by_game_id(
        game_id=game_id,
        language=language,
        sort=sort,
        period=period
    )

    if not videos:
        raise HTTPException(status_code=404, detail="No videos found for this game")

    return {"videos": videos}
