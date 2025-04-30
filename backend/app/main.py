from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.search import router as search_router
from app.api.autocomplete import router as autocomplete_router
from app.core.errors.handlers import setup_error_handlers

app = FastAPI(
    title="Twitch Video Searcher",
    description="Simple API to search Twitch videos by game name",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup error handlers
setup_error_handlers(app)

# Register routers
app.include_router(search_router, prefix="/api")
app.include_router(autocomplete_router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Twitch Video Searcher API",
        "docs": "/docs",
        "available_endpoints": [
            "/api/search - Search videos from Twitch API",
            "/api/videos - Search videos from database",
            "/api/autocomplete - Autocomplete game names"
        ]
    }
