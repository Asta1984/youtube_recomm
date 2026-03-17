from pydantic import BaseModel
from typing import List, Optional


class ChannelStatistics(BaseModel):
    view_count:               Optional[int]  = None
    subscriber_count:         Optional[int]  = None
    hidden_subscriber_count:  Optional[bool] = None
    video_count:              Optional[int]  = None


class ChannelDetail(BaseModel):
    channel_id:          str
    title:               str
    description:         Optional[str]       = None
    custom_url:          Optional[str]       = None
    country:             Optional[str]       = None
    published_at:        Optional[str]       = None
    thumbnail_url:       Optional[str]       = None
    uploads_playlist_id: Optional[str]       = None   # key field for pool_service
    topic_categories:    Optional[List[str]] = None   # e.g. "Science & Technology"
    statistics:          Optional[ChannelStatistics] = None


class ChannelListResponse(BaseModel):
    total:    int
    channels: List[ChannelDetail]
