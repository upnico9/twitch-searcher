from typing import Optional
import datetime
from fastapi import APIRouter, Query, Path
from app.services.twitch import TwitchService
from app.services.mongo_services import save_multiple_videos, get_videos_from_db
from app.models.models import Video
from app.core.errors.exceptions import ResourceNotFoundException, ValidationException

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
    if page < 1 or page_size < 1:
        raise ValidationException("Page and page_size must be positive integers")
    
    videos_data = twitch_service.get_videos_by_game_id(
        game_id=game_id,
        language=language,
        sort=sort,
        period=period
    )

    if not videos_data:
        raise ResourceNotFoundException("Videos", f"game_id: {game_id}")

    videos = [Video(**{**video, "game_id": game_id}) for video in videos_data]
    
    save_multiple_videos(videos)

    # Apply pagination
    start = (page - 1) * page_size
    end = start + page_size
    paginated_videos = videos_data[start:end]
    total_pages = -(-len(videos_data) // page_size)  # Ceiling division

    return {
        "videos": paginated_videos,
        "total": len(videos_data),
        "page": page,
        "page_size": page_size,
        "pages": total_pages
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
    if page < 1 or page_size < 1:
        raise ValidationException("Page and page_size must be positive integers")
    
    # Calculate pagination values
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
    
    total_pages = -(-result["total_count"] // page_size) if result["total_count"] > 0 else 0
    
    return {
        "videos": result["videos"],
        "total": result["total_count"],
        "page": page,
        "page_size": page_size,
        "pages": total_pages
    }


@router.get("/videos/{video_id}")
def get_video_by_id(
    video_id: str = Path(..., description="ID of the video to retrieve")
):
    video = get_videos_from_db(video_id=video_id)
    
    if not video:
        raise ResourceNotFoundException("Video", video_id)
    
    return video
