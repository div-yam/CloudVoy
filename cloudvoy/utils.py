import os
import logging
import requests
from datetime import timedelta
from .config import DOWNLOAD_PATH

def delete_local_file(file_path):
    """Deletes the local video file after successful upload."""
    try:
        os.remove(file_path)
        logging.info(f"Deleted local file: {file_path}")
    except OSError as e:
        logging.error(f"Error deleting local file {file_path}: {e}")

def get_thumbnail_url(video_id):
    """Retrieves the thumbnail URL for a given video ID."""
    thumbnail_url = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
    response = requests.head(thumbnail_url)
    if response.status_code != 200:
        logging.warning(f"Max resolution thumbnail not available for video ID: {video_id}. Trying default resolution.")
        thumbnail_url = f'https://img.youtube.com/vi/{video_id}/hqdefault.jpg'
        response = requests.head(thumbnail_url)
        if response.status_code != 200:
            logging.error(f"Thumbnail not available for video ID: {video_id}.")
            return None
    logging.info(f"Using thumbnail URL: {thumbnail_url}")
    return thumbnail_url

def get_ist_time(utc_time):
    """Converts UTC time to IST."""
    return utc_time + timedelta(hours=5, minutes=30)
