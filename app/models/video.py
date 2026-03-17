from pydantic import BaseModel
from typing import Dict, Optional, List
from datetime import datetime


class VideoItem(BaseModel):
    title: str
    video_id: str
    channel: str
    published_at: str
    url: str

class LikedVideosResponse(BaseModel):
    liked_videos: List[VideoItem]

class Thumbnail(BaseModel):
    url: str
    width: Optional[int] = None
    height: Optional[int] = None


class ResourceId(BaseModel):
    kind: str
    channelId: str


class Snippet(BaseModel):
    publishedAt: datetime
    channelTitle: str
    title: str
    description: str
    resourceId: ResourceId
    channelId: str
    thumbnails: Dict[str, Thumbnail]   # keys like default, medium, high


class ContentDetails(BaseModel):
    totalItemCount: int
    newItemCount: int
    activityType: Optional[str] = None


class SubscriberSnippet(BaseModel):
    title: str
    description: str
    channelId: str
    thumbnails: Dict[str, Thumbnail]


class SubscriptionResource(BaseModel):
    kind: str
    etag: str
    id: str
    snippet: Snippet
    contentDetails: ContentDetails
    subscriberSnippet: Optional[SubscriberSnippet] = None