import logging
import requests
import time
from .config import INSTAGRAM_ACCOUNT_ID, ACCESS_TOKEN
from .dynamodb_manager import save_video_details
from datetime import datetime
import json

def upload_reel(caption, video_url, cover_url):
    """Uploads a reel to Instagram using the provided video URL, caption, and cover image URL."""
    logging.info("Uploading reel to Instagram...")
    upload_url = f"https://graph.facebook.com/v17.0/{INSTAGRAM_ACCOUNT_ID}/media"
    payload = {
        'media_type': 'REELS',
        'video_url': video_url,
        'caption': caption,
        'cover_url': cover_url,
        'access_token': ACCESS_TOKEN
    }
    r = requests.post(upload_url, data=payload)
    logging.info(f"Instagram upload response: {r.text}")
    try:
        results = r.json()
    except json.JSONDecodeError:
        logging.error("Failed to parse Instagram response as JSON.")
        return {}
    return results

def get_status_code(ig_container_id):
    """Checks the status of the Instagram media upload."""
    logging.info(f"Checking status for container ID: {ig_container_id}")
    url = f'https://graph.facebook.com/v17.0/{ig_container_id}'
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'status_code'
    }
    response = requests.get(url, params=params)
    try:
        response_json = response.json()
    except json.JSONDecodeError:
        logging.error("Failed to parse status response as JSON.")
        return 'unknown_error'
    status = response_json.get('status_code')
    logging.info(f"Status code: {status}")
    return status

def publish_video(creation_id):
    """Publishes the video to Instagram Reels using the provided creation ID."""
    logging.info("Publishing video to Instagram Reels...")
    url = f'https://graph.facebook.com/v17.0/{INSTAGRAM_ACCOUNT_ID}/media_publish'
    payload = {
        'creation_id': creation_id,
        'access_token': ACCESS_TOKEN
    }
    response = requests.post(url, data=payload)
    try:
        response_json = response.json()
    except json.JSONDecodeError:
        logging.error("Failed to parse publish response as JSON.")
        return {}
    if 'id' in response_json:
        logging.info(f"Video published successfully. Media ID: {response_json['id']}")
    else:
        logging.error(f"Failed to publish video: {response_json}")
    return response_json
