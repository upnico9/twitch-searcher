from fastapi import FastAPI

from app.api.search import router as search_router
from app.api.autocomplete import router as autocomplete_router

app = FastAPI(
        title="Twitch Video Searcher",
        description="Simple API to search Twitch videos by game name",
        version="0.1.0",
    )

app.include_router(search_router, prefix="/api")
app.include_router(autocomplete_router, prefix="/api")