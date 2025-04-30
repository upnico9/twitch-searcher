from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime

# Modèles de base
class Game(BaseModel):
    """Représentation d'un jeu sur Twitch"""
    id: str = Field(..., description="Identifiant unique du jeu")
    name: str = Field(..., description="Nom du jeu")
    box_art_url: str = Field(..., description="URL de l'image du jeu")

class VideoBase(BaseModel):
    """Modèle de base pour les vidéos Twitch"""
    id: str = Field(..., description="Identifiant unique de la vidéo")
    user_name: str = Field(..., description="Nom du créateur de la vidéo")
    title: str = Field(..., description="Titre de la vidéo")
    description: Optional[str] = Field(None, description="Description de la vidéo")
    created_at: datetime = Field(..., description="Date de création")
    published_at: datetime = Field(..., description="Date de publication")
    url: str = Field(..., description="URL de la vidéo")
    thumbnail_url: str = Field(..., description="URL de la miniature")
    viewable: str = Field(..., description="Visibilité de la vidéo")
    view_count: int = Field(..., description="Nombre de vues")
    language: str = Field(..., description="Langue de la vidéo")
    type: str = Field(..., description="Type de vidéo")
    duration: str = Field(..., description="Durée de la vidéo")

class VideoResponse(VideoBase):
    """Modèle complet d'une vidéo avec l'ID du jeu"""
    game_id: str = Field(..., description="Identifiant du jeu associé")

# Réponses d'API
class PaginatedResponse(BaseModel):
    """Base pour les réponses paginées"""
    total: int = Field(..., description="Nombre total d'éléments")
    page: int = Field(..., description="Numéro de page actuel")
    page_size: int = Field(..., description="Nombre d'éléments par page")
    pages: int = Field(..., description="Nombre total de pages")

class VideoListResponse(PaginatedResponse):
    """Liste paginée de vidéos"""
    videos: List[Dict[str, Any]] = Field(..., description="Liste des vidéos")

class AutocompleteResponse(BaseModel):
    """Résultat d'une recherche d'autocomplétion"""
    games: List[Game] = Field(..., description="Liste des jeux correspondants")

# Modèles d'erreur
class ErrorDetail(BaseModel):
    """Détail d'une erreur"""
    loc: Optional[List[str]] = Field(None, description="Localisation de l'erreur")
    msg: str = Field(..., description="Message d'erreur")
    type: str = Field(..., description="Type d'erreur")

class ErrorResponse(BaseModel):
    """Réponse d'erreur standard"""
    code: str = Field(..., description="Code d'erreur")
    message: str = Field(..., description="Message d'erreur")
    status: int = Field(..., description="Code de statut HTTP")
    details: Optional[List[ErrorDetail]] = Field(None, description="Détails additionnels")