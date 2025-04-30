from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from bson import ObjectId

def generate_object_id() -> str:
    return str(ObjectId())

class Video(BaseModel):
    mongo_id: Optional[str] = Field(default_factory=generate_object_id, alias="_id")
    id: str
    stream_id: Optional[str] = None
    user_id: str
    user_login: Optional[str] = None
    user_name: str
    title: str
    description: Optional[str] = None
    created_at: str
    published_at: str
    url: str
    thumbnail_url: str
    viewable: str
    view_count: int
    language: str
    type: str
    duration: str
    muted_segments: Optional[List[Dict[str, Any]]] = None
    game_id: Optional[str] = None
    tag_ids: Optional[List[str]] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

    def to_mongo_dict(self) -> Dict[str, Any]:
        mongo_dict = {
            k: v for k, v in self.dict(by_alias=True).items()
            if k != "_id" and v is not None and v != ""
        }
        
        if "thumbnail_url" in mongo_dict and "%{" in mongo_dict["thumbnail_url"]:
            mongo_dict["thumbnail_url"] = mongo_dict["thumbnail_url"].replace("%{width}", "1920").replace("%{height}", "1080")
        
        return mongo_dict