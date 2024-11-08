import os
import logging
import yt_dlp
from .config import DOWNLOAD_PATH

# Ensure the download directory exists
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

def download_video(video_url, filename):
    """Downloads a video from YouTube."""
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
            'outtmpl': os.path.join(DOWNLOAD_PATH, f'{filename}.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'merge_output_format': 'mp4',
            'cookiefile': 'all_cookies.txt'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', None)
            logging.info(f"Downloaded: {video_title}")
            return True
    except Exception as e:
        logging.error(f"An error occurred while downloading {video_url}: {e}")
        return False
