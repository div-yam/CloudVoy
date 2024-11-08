import logging
from googleapiclient.discovery import build
from .config import (
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    YOUTUBE_API_KEY,
    PLAYLIST_ID
)

def get_playlist_videos(max_results=1):
    """Fetches videos from the specified YouTube playlist."""
    logging.info("Fetching playlist videos...")
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=PLAYLIST_ID,
        maxResults=max_results
    )
    response = request.execute()
    videos = []
    for item in response.get('items', []):
        video_id = item['snippet']['resourceId']['videoId']
        video_title = item['snippet']['title']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        video_upload_date = item['snippet']['publishedAt']  # Extract upload date
        videos.append({
            'title': video_title,
            'video_id': video_id,
            'video_url': video_url,
            'published_at': video_upload_date
        })
    logging.info(f"Found {len(videos)} videos in the playlist.")
    return videos
