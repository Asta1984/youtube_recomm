from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
from app.services import youtube_service, subscriptions_service, channel_service
from app.models.video import LikedVideosResponse
from app.models.subscription import SubscriptionsResponse, SubscribedChannel
from app.models.channel import ChannelListResponse
from app.db import session_store

router = APIRouter(tags=["YouTube"])


def _check_auth():
    """Reusable auth check — redirects to /login if no token."""
    if not session_store.get("token"):
        return RedirectResponse("/login")
    return None


# ── Liked Videos ──────────────────────────────────────────────────────────────
@router.get("/liked-videos", response_model=LikedVideosResponse)
def get_liked_videos(max_results: int = Query(default=20, ge=1, le=50)):
    """Return the authenticated user's liked videos."""
    if redirect := _check_auth():
        return redirect

    videos = youtube_service.get_liked_videos(max_results=max_results)
    return LikedVideosResponse(liked_videos=videos)


# ── Subscriptions ─────────────────────────────────────────────────────────────
@router.get("/subscriptions", response_model=SubscriptionsResponse)
def get_subscriptions():
    """Return all channels the authenticated user subscribes to."""
    if redirect := _check_auth():
        return redirect

    try:
        raw = subscriptions_service.fetch_all_subscriptions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch subscriptions: {str(e)}")

    channels = [
        SubscribedChannel(
            channel_id       = item["snippet"]["resourceId"]["channelId"],
            name             = item["snippet"]["title"],
            description      = item["snippet"].get("description"),
            subscribed_since = item["snippet"].get("publishedAt"),
            thumbnail_url    = item["snippet"]["thumbnails"]["default"]["url"]
        )
        for item in raw
    ]

    return SubscriptionsResponse(total=len(channels), channels=channels)


# ── Channel Details ───────────────────────────────────────────────────────────
@router.get("/channels", response_model=ChannelListResponse)
def get_subscribed_channel_details():
    """
    Return full details of all subscribed channels.
    Chains subscriptions_service → channel_service internally.
    """
    if redirect := _check_auth():
        return redirect

    try:
        channel_ids = subscriptions_service.get_subscribed_channel_ids()
        channels    = channel_service.get_channel_details(channel_ids)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch channel details: {str(e)}")

    return ChannelListResponse(total=len(channels), channels=channels)


# ── Single Channel ────────────────────────────────────────────────────────────
@router.get("/channels/{channel_id}", response_model=ChannelListResponse)
def get_channel_by_id(channel_id: str):
    """Return details for a single channel by its ID."""
    if redirect := _check_auth():
        return redirect

    try:
        channels = channel_service.get_channel_details([channel_id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch channel: {str(e)}")

    if not channels:
        raise HTTPException(status_code=404, detail=f"Channel {channel_id} not found")

    return ChannelListResponse(total=1, channels=channels)