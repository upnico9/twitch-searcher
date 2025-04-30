from fastapi import APIRouter, Query, status
from app.services.twitch import TwitchService
from app.core.errors.exceptions import ResourceNotFoundException
from app.api.schemas import AutocompleteResponse

router = APIRouter()
twitch_service = TwitchService()

@router.get(
    "/autocomplete",
    response_model=AutocompleteResponse,
    summary="Autocomplétion des noms de jeux",
    description="Recherche et suggère des jeux dont le nom correspond à la requête",
    response_description="Liste de jeux correspondants avec leurs identifiants"
)
def autocomplete_games(
    game: str = Query(
        ..., 
        description="Nom partiel du jeu à rechercher",
        min_length=2,
        example="League"
    )
):
    """
    Recherche des jeux sur Twitch dont le nom correspond partiellement à la requête.
    
    - **game**: Texte de recherche (min. 2 caractères)
    
    Retourne une liste de jeux correspondants avec leurs identifiants.
    """
    games = twitch_service.autocomplete_games(game)
    
    if not games:
        raise ResourceNotFoundException("Games", f"matching query: {game}")
    
    return {"games": games}
