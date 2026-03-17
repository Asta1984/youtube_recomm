from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from app.core.config import API_SERVICE_NAME, API_VERSION
from app.db import session_store
from typing import List


def _get_youtube_client():
    token = session_store.get("token")
    creds = Credentials(token=token)
    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)


def fetch_all_subscriptions() -> List[dict]:
    """
    Fetch all channels the authenticated user subscribes to.
    Handles pagination automatically — returns every subscription,
    not just the first 50.
    """
    youtube = _get_youtube_client()
    subscriptions = []
    next_page_token = None

    while True:
        response = youtube.subscriptions().list(
            part="snippet",
            mine=True,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        subscriptions += response.get("items", [])
        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return subscriptions


def get_subscribed_channel_ids() -> List[str]:
    """Return just the channel IDs — used to feed into channel_service."""
    subscriptions = fetch_all_subscriptions()
    return [
        item["snippet"]["resourceId"]["channelId"]
        for item in subscriptions
    ]


def get_subscription_count() -> int:
    """Return total number of subscriptions."""
    return len(fetch_all_subscriptions())
