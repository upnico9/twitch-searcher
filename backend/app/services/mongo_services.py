from typing import List, Dict, Any, Optional
import datetime
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from app.db.mongo import get_collection
from app.models.models import Video
from app.core.errors.exceptions import DatabaseException, ResourceNotFoundException

video_collection: Collection = get_collection() 

def save_video(video: Video):
    try:
        video_dict = video.dict()
        video_collection.update_one({"id": video.id}, {"$set": video_dict}, upsert=True)
    except PyMongoError as e:
        raise DatabaseException(operation="save", detail=str(e))

def get_videos():
    try:
        videos = list(video_collection.find({}, {"_id": 0}))
        return videos
    except PyMongoError as e:
        raise DatabaseException(operation="find", detail=str(e))

def save_multiple_videos(videos: List[Video]):
    success_count = 0
    error_count = 0
    
    for i, video in enumerate(videos):
        clean_data = video.to_mongo_dict()
        
        if "thumbnail_url" in clean_data and "%{" in clean_data["thumbnail_url"]:
            clean_data["thumbnail_url"] = clean_data["thumbnail_url"].replace("%{width}", "1920").replace("%{height}", "1080")
        
        try:
            print(f"Inserting video {i+1}/{len(videos)} with ID {video.id}")
            video_collection.update_one(
                {"id": video.id},
                {"$set": clean_data},
                upsert=True
            )
            success_count += 1
            print(f"Video {i+1} inserted successfully")
        except PyMongoError as e:
            error_count += 1
            print(f"Error inserting video {i+1}: {str(e)}")
    
    print(f"Bulk insertion completed: {success_count} success, {error_count} errors")
    if error_count > 0 and success_count == 0:
        raise DatabaseException(operation="batch_insert", detail=f"All {error_count} insertions failed")
    
    return {
        "success_count": success_count,
        "error_count": error_count
    }

def get_videos_from_db(
    video_id: Optional[str] = None,
    game_id: Optional[str] = None,
    language: Optional[str] = None,
    sort: Optional[str] = None,
    period: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
) -> Dict[str, Any]:
    """
    Retrieves videos from the database with optional filters.
    
    Args:
        video_id: Specific video ID to retrieve
        game_id: Filter by game ID
        language: Filter by language (e.g. 'en', 'fr')
        sort: Sort by 'time', 'trending' or 'views'
        period: Filter by 'day', 'week', 'month', or 'all'
        skip: Number of videos to skip (for pagination)
        limit: Maximum number of videos to return
        
    Returns:
        Dictionary containing videos and total count
    """
    try:
        filter_query = {}
        
        if video_id:
            result = video_collection.find_one({"id": video_id}, {"_id": 0})
            if not result:
                raise ResourceNotFoundException("Video", video_id)
            return result
        
        if game_id:
            filter_query["game_id"] = game_id
        
        if language:
            filter_query["language"] = language
        
        if period:
            now = datetime.datetime.utcnow()
            if period == "day":
                date_limit = now - datetime.timedelta(days=1)
            elif period == "week":
                date_limit = now - datetime.timedelta(weeks=1)
            elif period == "month":
                date_limit = now - datetime.timedelta(days=30)
            else:
                date_limit = None
                
            if date_limit:
                date_str = date_limit.strftime("%Y-%m-%dT%H:%M:%SZ")
                filter_query["created_at"] = {"$gte": date_str}
        
        sort_options = []
        if sort == "time":
            sort_options = [("created_at", -1)]
        elif sort == "views":
            sort_options = [("view_count", -1)]
        elif sort == "trending":
            sort_options = [("view_count", -1), ("created_at", -1)]
        
        total_count = video_collection.count_documents(filter_query)
        
        cursor = video_collection.find(filter_query, {"_id": 0})
        
        if sort_options:
            cursor = cursor.sort(sort_options)
        
        videos = list(cursor.skip(skip).limit(limit))
        
        return {
            "videos": videos,
            "total_count": total_count
        }
    except ResourceNotFoundException:
        raise
    except PyMongoError as e:
        raise DatabaseException(operation="query", detail=str(e))
    except Exception as e:
        raise DatabaseException(operation="query", detail="Unexpected error occurred")