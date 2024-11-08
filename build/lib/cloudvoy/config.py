import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# YouTube Data API configuration
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
PLAYLIST_ID = os.getenv("YOUTUBE_PLAYLIST_ID")

# Instagram Graph API configuration
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
AWS_S3_REGION = os.getenv("AWS_S3_REGION")

# DynamoDB configuration
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")

# Other configurations
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "downloaded_videos")
