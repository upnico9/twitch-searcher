from typing import Optional
from fastapi import APIRouter, Query, Path, status
from app.services.twitch import TwitchService
from app.services.mongo_services import save_multiple_videos, get_videos_from_db
from app.models.models import Video
from app.core.errors.exceptions import ResourceNotFoundException, ValidationException
from app.api.schemas import VideoListResponse, VideoResponse

router = APIRouter()
twitch_service = TwitchService()

@router.get(
    "/search",
    response_model=VideoListResponse,
    summary="Rechercher des vidéos Twitch par jeu",
    description="""
    Recherche des vidéos sur Twitch pour un jeu spécifique.
    
    Les résultats peuvent être filtrés par langue et période, et triés selon différents critères.
    Les vidéos trouvées sont automatiquement sauvegardées dans la base de données.
    """,
    response_description="Liste paginée de vidéos Twitch"
)
def search_videos(
    game_id: str = Query(..., description="ID du jeu à rechercher", example="21779"),
    language: Optional[str] = Query(None, description="Filtrer par langue (ex: 'fr', 'en')"),
    sort: Optional[str] = Query(None, description="Trier par 'time', 'trending' ou 'views'"),
    period: Optional[str] = Query(None, description="Filtrer par 'day', 'week', 'month', ou 'all'"),
    page: int = Query(1, description="Numéro de page, à partir de 1", ge=1),
    page_size: int = Query(20, description="Nombre de vidéos par page", ge=1, le=100)
):
    """
    Recherche des vidéos sur Twitch pour un jeu spécifique avec différentes options de filtrage.
    
    - **game_id**: Identifiant du jeu sur Twitch
    - **language**: Code de langue (fr, en, etc.)
    - **sort**: Méthode de tri (time, trending, views)
    - **period**: Période de recherche (day, week, month, all)
    - **page**: Numéro de la page pour la pagination
    - **page_size**: Nombre d'éléments par page
    """
    if page < 1 or page_size < 1:
        raise ValidationException("Page et page_size doivent être des entiers positifs")
    
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


@router.get(
    "/videos",
    response_model=VideoListResponse,
    summary="Récupérer les vidéos enregistrées",
    description="Récupère les vidéos sauvegardées dans la base de données avec possibilité de filtrage.",
    response_description="Liste paginée de vidéos depuis la base de données"
)
def get_videos(
    game_id: Optional[str] = Query(None, description="Filtrer par ID de jeu"),
    language: Optional[str] = Query(None, description="Filtrer par langue (ex: 'fr', 'en')"),
    sort: Optional[str] = Query(None, description="Trier par 'time', 'trending' ou 'views'"),
    period: Optional[str] = Query(None, description="Filtrer par 'day', 'week', 'month', ou 'all'"),
    page: int = Query(1, description="Numéro de page, à partir de 1", ge=1),
    page_size: int = Query(20, description="Nombre de vidéos par page", ge=1, le=100)
):
    """
    Récupère les vidéos enregistrées dans la base de données avec différentes options de filtrage.
    
    - **game_id**: Filtrer par identifiant du jeu
    - **language**: Filtrer par langue
    - **sort**: Méthode de tri
    - **period**: Filtrer par période
    - **page**: Numéro de page pour la pagination
    - **page_size**: Nombre d'éléments par page
    """
    if page < 1 or page_size < 1:
        raise ValidationException("Page et page_size doivent être des entiers positifs")
    
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


@router.get(
    "/videos/{video_id}",
    response_model=VideoResponse,
    summary="Récupérer une vidéo par ID",
    description="Récupère les détails d'une vidéo spécifique par son identifiant.",
    response_description="Détails complets d'une vidéo"
)
def get_video_by_id(
    video_id: str = Path(..., description="ID de la vidéo à récupérer")
):
    """
    Récupère une vidéo spécifique par son ID.
    
    - **video_id**: Identifiant unique de la vidéo
    
    Retourne les détails complets de la vidéo si elle existe.
    """
    video = get_videos_from_db(video_id=video_id)
    
    if not video:
        raise ResourceNotFoundException("Video", video_id)
    
    return video
