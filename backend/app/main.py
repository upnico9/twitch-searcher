from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.search import router as search_router
from app.api.autocomplete import router as autocomplete_router

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

app.include_router(search_router, prefix="/api")
app.include_router(autocomplete_router, prefix="/api")