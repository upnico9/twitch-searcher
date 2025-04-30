from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api.search import router as search_router
from app.api.autocomplete import router as autocomplete_router
from app.core.errors.handlers import setup_error_handlers

app = FastAPI(
    title="Twitch Video Searcher API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_error_handlers(app)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    openapi_schema["tags"] = [
        {
            "name": "recherche",
            "description": "Endpoints pour la recherche de vidéos",
        },
        {
            "name": "autocomplete",
            "description": "Endpoints pour la suggestion de jeux",
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(
    search_router,
    prefix="/api",
    tags=["recherche"],
)

app.include_router(
    autocomplete_router,
    prefix="/api",
    tags=["autocomplete"],
)

@app.get("/", tags=["info"])
def read_root():
    """
    Page d'accueil de l'API avec liens vers la documentation.
    """
    return {
        "message": "Bienvenue sur l'API Twitch Video Searcher",
        "documentation": "/docs",
        "endpoints_disponibles": [
            "/api/search - Recherche de vidéos via l'API Twitch",
            "/api/videos - Recherche de vidéos depuis la base de données",
            "/api/autocomplete - Autocomplétion des noms de jeux"
        ]
    }
