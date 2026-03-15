from pydantic import BaseModel
from typing import List, Optional

class VideoItem(BaseModel):
    title: str
    video_id: str
    channel: str
    published_at: str
    url: str


class Thumbnail(BaseModel):
    url: str
    width: int
    height: int

class ContentDetails(BaseModel):
        totalItemCount:int
        newItemCount: int
        activityType: str

class SubscriberSnippet(BaseModel):
         title: str
         description: str
         channelId: str
         thumbnails: Thumbnail
     
class PageInfo(BaseModel):
    totalResults: int
    resultsPerPage: int

class SubscriptionResource(BaseModel):
    id: Optional[str]
    kind: Optional[str] 

class ResourceId(BaseModel):
     kind: str
     channel_id = str

class Subscription_list(BaseModel):



class LikedVideosResponse(BaseModel):
    liked_videos: List[VideoItem]