from pydantic import BaseModel
from typing import List, Optional


class SubscribedChannel(BaseModel):
    channel_id:       str
    name:             str
    description:      Optional[str] = None
    subscribed_since: Optional[str] = None
    thumbnail_url:    Optional[str] = None


class SubscriptionsResponse(BaseModel):
    total:    int
    channels: List[SubscribedChannel]