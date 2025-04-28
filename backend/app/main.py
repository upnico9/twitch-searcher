from fastapi import FastAPI
from app.core.config import get_settings

app = FastAPI()

settings = get_settings()

# Print settings to check if they are loaded correctly
print("settings", settings)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}