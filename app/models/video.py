from pydantic import BaseModel
from typing import List


class VideoItem(BaseModel):
    title: str
    video_id: str
    channel: str
    published_at: str
    url: str


class LikedVideosResponse(BaseModel):
    liked_videos: List[VideoItem]