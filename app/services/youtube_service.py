from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from app.core.config import API_SERVICE_NAME, API_VERSION
from app.db import session_store
from app.models.video import VideoItem
from typing import List


def get_liked_videos(max_results: int = 20) -> List[VideoItem]:
    """Fetch the authenticated user's liked videos from YouTube API."""

    token = session_store.get("token")
    creds = Credentials(token=token)

    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=creds)

    response = youtube.videos().list(
        part="snippet,contentDetails",
        myRating="like",
        maxResults=max_results
    ).execute()

    return [
        VideoItem(
            title=item["snippet"]["title"],
            video_id=item["id"],
            channel=item["snippet"]["channelTitle"],
            published_at=item["snippet"]["publishedAt"],
            url=f"https://www.youtube.com/watch?v={item['id']}"
        )
        for item in response.get("items", [])
    ]