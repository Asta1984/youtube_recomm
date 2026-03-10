from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.services import youtube_service
from app.models.video import LikedVideosResponse
from app.db import session_store

router = APIRouter(tags=["YouTube"])


@router.get("/liked-videos", response_model=LikedVideosResponse)
def get_liked_videos():
    """Return the authenticated user's liked videos."""
    if not session_store.get("token"):
        return RedirectResponse("/login")

    videos = youtube_service.get_liked_videos(max_results=20)
    return LikedVideosResponse(liked_videos=videos)