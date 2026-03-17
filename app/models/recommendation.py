from pydantic import BaseModel
from typing import List


class RecommendedVideo(BaseModel):
    title: str
    video_id: str
    channel: str
    url: str
    published_at: str
    similarity_score: float


class RecommendationResponse(BaseModel):
    total: int
    recommendations: List[RecommendedVideo]