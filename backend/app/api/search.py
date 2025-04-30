from typing import Optional
import datetime
from fastapi import APIRouter, Query, HTTPException, Path
from app.services.twitch import TwitchService
from app.services.mongo_services import save_multiple_videos, get_videos_from_db
from app.models.models import Video

router = APIRouter()
twitch_service = TwitchService()

@router.get("/search")
def search_videos(
    game_id: str = Query(..., description="Game ID to search videos for"),
    language: Optional[str] = Query(None, description="Filter by language (e.g. 'en', 'fr')"),
    sort: Optional[str] = Query(None, description="Sort by 'time', 'trending' or 'views'"),
    period: Optional[str] = Query(None, description="Filter by 'day', 'week', 'month', or 'all'"),
    page: int = Query(1, description="Page number, starting from 1"),
    page_size: int = Query(20, description="Number of videos per page")
):
    videos_data = twitch_service.get_videos_by_game_id(
        game_id=game_id,
        language=language,
        sort=sort,
        period=period
    )

    if not videos_data:
        raise HTTPException(status_code=404, detail="No videos found for this game")

    videos = [Video(**{**video, "game_id": game_id}) for video in videos_data]

    save_multiple_videos(videos)

    start = (page - 1) * page_size
    end = start + page_size
    paginated_videos = videos_data[start:end]

    return {
        "videos": paginated_videos,
        "total": len(videos_data),
        "page": page,
        "page_size": page_size,
        "pages": -(-len(videos_data) // page_size) 
    }


@router.get("/videos")
def get_videos(
    game_id: Optional[str] = Query(None, description="Filter by game ID"),
    language: Optional[str] = Query(None, description="Filter by language (e.g. 'en', 'fr')"),
    sort: Optional[str] = Query(None, description="Sort by 'time', 'trending' or 'views'"),
    period: Optional[str] = Query(None, description="Filter by 'day', 'week', 'month', or 'all'"),
    page: int = Query(1, description="Page number, starting from 1"),
    page_size: int = Query(20, description="Number of videos per page")
):

    skip = (page - 1) * page_size
    limit = page_size
    
    result = get_videos_from_db(
        game_id=game_id,
        language=language,
        sort=sort,
        period=period,
        skip=skip,
        limit=limit
    )
    
    return {
        "videos": result["videos"],
        "total": result["total_count"],
        "page": page,
        "page_size": page_size,
        "pages": -(-result["total_count"] // page_size)
    }
