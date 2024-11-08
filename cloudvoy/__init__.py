import logging
import os
import time
from datetime import datetime, timedelta
from .youtube import get_playlist_videos
from .downloader import download_video
from .s3_uploader import upload_file_to_s3, delete_file_from_s3
from .instagram_uploader import upload_reel, get_status_code, publish_video
from .dynamodb_manager import save_video_details, get_upload_status
from .utils import delete_local_file, get_thumbnail_url, get_ist_time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def upload_to_instagram_using_link(video_url, video_id=None, title=None):
    """
    Uploads a single video to Instagram using the provided YouTube link.

    Parameters:
        video_url (str): The YouTube video URL.
        video_id (str, optional): The YouTube video ID. If not provided, it will be extracted from the URL.
        title (str, optional): The caption for the Instagram reel. If not provided, the video title from YouTube will be used.
    """
    if not video_id:
        try:
            video_id = video_url.split('v=')[-1]
        except IndexError:
            logging.error("Invalid YouTube URL provided.")
            return

    if not title:
        # Fetch video details from YouTube
        videos = get_playlist_videos(max_results=1)
        if not videos:
            logging.error("No videos found to fetch the title.")
            return
        title = videos[0]['title']

    # Check upload status from DynamoDB
    upload_status = get_upload_status(video_id)
    if upload_status == 'success':
        logging.info(f"Video ID {video_id} has already been uploaded successfully. Skipping.")
        return
    elif upload_status == 'pending':
        logging.info(f"Video ID {video_id} upload is currently pending. Skipping.")
        return
    else:
        logging.info(f"Video ID {video_id} has not been uploaded yet. Proceeding with upload.")

    # Set upload_status to 'pending' before starting the upload process
    video_upload_date = datetime.utcnow().isoformat()
    save_video_details(
        video_id=video_id,
        upload_status='pending',
        instagram_publish_time=None,
        video_upload_date=video_upload_date,
        title=title
    )

    # Download the video
    download_success = download_video(video_url, video_id)
    file_path = os.path.join("downloaded_videos", f"{video_id}.mp4")

    if download_success:
        # Upload to AWS S3
        s3_key = f"{video_id}.mp4"
        s3_url = upload_file_to_s3(file_path, s3_key)
        if not s3_url:
            # Update DynamoDB to indicate failure
            save_video_details(
                video_id=video_id,
                upload_status='failed',
                instagram_publish_time=None,
                video_upload_date=video_upload_date
            )
            return

        # Get thumbnail URL
        thumbnail_url = get_thumbnail_url(video_id)
        if not thumbnail_url:
            # Update DynamoDB to indicate failure
            save_video_details(
                video_id=video_id,
                upload_status='failed',
                instagram_publish_time=None,
                video_upload_date=video_upload_date
            )
            return

        # Upload to Instagram Reels
        results = upload_reel(title, s3_url, thumbnail_url)
        upload_success = 'id' in results

        if not upload_success:
            logging.error("Failed to upload reel to Instagram.")
            save_video_details(
                video_id=video_id,
                upload_status='failed',
                instagram_publish_time=None,
                video_upload_date=video_upload_date
            )
            return

        ig_container_id = results.get('id')

        # Check the status repeatedly until it's FINISHED or an error occurs
        max_retries = 10    # Maximum number of retries
        retry_delay = 10    # Delay in seconds between retries
        for attempt in range(max_retries):
            status = get_status_code(ig_container_id)
            if status == 'FINISHED':
                # Publish the video
                publish_response = publish_video(ig_container_id)
                logging.info(f"Publish response: {publish_response}")

                # Get the current date and time for the Instagram publish time
                instagram_publish_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

                # Save details to DynamoDB
                save_video_details(
                    video_id=video_id,
                    upload_status='success',
                    instagram_publish_time=instagram_publish_time,
                    video_upload_date=video_upload_date
                )

                # Delete the video from S3
                delete_file_from_s3(s3_key)

                # Delete the local video file
                delete_local_file(file_path)

                break
            elif status == 'ERROR':
                logging.error("Error occurred during media processing.")
                save_video_details(
                    video_id=video_id,
                    upload_status='failed',
                    instagram_publish_time=None,
                    video_upload_date=video_upload_date
                )
                break
            else:
                logging.info(f"Status is '{status}'. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
        else:
            logging.error("Exceeded maximum retries. Video could not be published.")
            save_video_details(
                video_id=video_id,
                upload_status='failed',
                instagram_publish_time=None,
                video_upload_date=video_upload_date
            )
    else:
        logging.error(f"Skipping upload for video ID: {video_id}")
        save_video_details(
            video_id=video_id,
            upload_status='failed',
            instagram_publish_time=None,
            video_upload_date=video_upload_date
        )

def upload_instagram_today_videos():
    """
    Uploads all videos from the YouTube playlist that were uploaded today (IST) to Instagram.
    """
    ist_today = datetime.utcnow() + timedelta(hours=5, minutes=30)
    start_of_day = ist_today.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = ist_today.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Fetch up to 50 videos; adjust as needed
    videos = get_playlist_videos(max_results=50)
    logging.info(f"Found {len(videos)} videos in the playlist.")

    for video in videos:
        video_id = video['video_id']
        video_upload_date = datetime.fromisoformat(video['published_at'].replace('Z', '+00:00'))
        uploaded_ist_time = get_ist_time(video_upload_date)

        if start_of_day <= uploaded_ist_time <= end_of_day:
            logging.info(f"Processing video uploaded today: {video_id}")
            upload_to_instagram_using_link(video['video_url'], video_id, video['title'])

    logging.info("All videos uploaded today have been processed.")
