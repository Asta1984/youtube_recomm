from googleapiclient.discovery import build
from app.core.config import API_SERVICE_NAME, API_VERSION, API_KEY
from app.models.channel import ChannelDetail, ChannelStatistics
from typing import List


def _get_youtube_client():
    """Unauthenticated client — channel details are public data."""
    return build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)


def get_channel_details(channel_ids: List[str]) -> List[ChannelDetail]:
    """
    Fetch full channel details for a list of channel IDs.
    Batches into groups of 50 (YouTube API limit per request).

    Returns: descriptions, uploads_playlist_id, topic_categories,
             statistics — everything needed for the recommender.
    """
    youtube = _get_youtube_client()
    all_channels = []

    # YouTube allows max 50 IDs per request — batch accordingly
    for i in range(0, len(channel_ids), 50):
        batch = channel_ids[i:i + 50]

        response = youtube.channels().list(
            part="snippet,contentDetails,statistics,topicDetails",
            id=",".join(batch)
        ).execute()

        all_channels += _parse_channel_items(response.get("items", []))

    return all_channels


def get_channel_descriptions(channel_ids: List[str]) -> List[str]:
    """
    Return just descriptions — used by embedding_service
    to build the user vector.
    Falls back to channel title if description is empty.
    """
    channels = get_channel_details(channel_ids)
    return [
        c.description if c.description else c.title
        for c in channels
    ]


def get_uploads_playlist_ids(channel_ids: List[str]) -> List[str]:
    """
    Return uploads playlist IDs — used by pool_service
    to fetch latest videos from each subscribed channel.
    """
    channels = get_channel_details(channel_ids)
    return [
        c.uploads_playlist_id
        for c in channels
        if c.uploads_playlist_id
    ]


def _parse_channel_items(items: List[dict]) -> List[ChannelDetail]:
    """Map raw YouTube API response items to ChannelDetail models."""
    result = []

    for item in items:
        snippet    = item.get("snippet", {})
        stats      = item.get("statistics", {})
        content    = item.get("contentDetails", {}).get("relatedPlaylists", {})
        topics     = item.get("topicDetails", {}).get("topicCategories", [])
        thumbnails = snippet.get("thumbnails", {})
        thumb_url  = thumbnails.get("default", {}).get("url")

        result.append(ChannelDetail(
            channel_id          = item["id"],
            title               = snippet.get("title", ""),
            description         = snippet.get("description", ""),
            custom_url          = snippet.get("customUrl"),
            country             = snippet.get("country"),
            published_at        = snippet.get("publishedAt"),
            thumbnail_url       = thumb_url,
            uploads_playlist_id = content.get("uploads"),
            topic_categories    = topics,
            statistics          = ChannelStatistics(
                view_count              = stats.get("viewCount"),
                subscriber_count        = stats.get("subscriberCount"),
                hidden_subscriber_count = stats.get("hiddenSubscriberCount", False),
                video_count             = stats.get("videoCount"),
            )
        ))

    return result
