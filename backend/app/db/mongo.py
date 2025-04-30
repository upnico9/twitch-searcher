from pymongo import MongoClient, ASCENDING
from app.core.config import get_settings

settings = get_settings()

client = MongoClient(settings.mongodb_uri)
db = client[settings.mongodb_db_name]

video_collection = db["videos"]
video_collection.create_index([("id", ASCENDING)], unique=True)

def get_collection():
    return video_collection