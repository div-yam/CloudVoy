# CloudVoy

CloudVoy is a robust Python library designed to automate the process of uploading YouTube videos to Instagram Reels. By seamlessly integrating with the YouTube Data API, AWS S3, Instagram Graph API, and AWS DynamoDB, CloudVoy provides a streamlined workflow for content creators to distribute their YouTube content to Instagram effortlessly.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [1. Upload a Single Video Using a YouTube Link](#1-upload-a-single-video-using-a-youtube-link)
  - [2. Upload All Today's Videos from Your Playlist](#2-upload-all-todays-videos-from-your-playlist)
- [Examples](#examples)
- [Testing](#testing)
- [Contributing](#contributing)

---

## Features

- **Automated Workflow**: Fetches videos from a specified YouTube playlist, downloads them, uploads to AWS S3, and publishes them as Instagram Reels.
- **Status Tracking**: Utilizes AWS DynamoDB to track the upload status of each video, preventing duplicate uploads.
- **Thumbnail Management**: Automatically retrieves and validates YouTube video thumbnails for Instagram Reels.
- **Error Handling & Logging**: Comprehensive logging to monitor the upload process and handle errors gracefully.
- **Scalable & Secure**: Leverages AWS services for scalable storage and secure handling of credentials.

## Prerequisites

Before using CloudVoy, ensure you have the following:

1. **Python 3.6 or Higher**: Ensure Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
2. **YouTube Data API Key**: Obtain an API key from the [Google Developers Console](https://console.developers.google.com/).
3. **Instagram Graph API Credentials**: Set up a Facebook Developer account and obtain the necessary credentials to interact with the Instagram Graph API.
4. **AWS Account**: Access to AWS services including S3 and DynamoDB. You'll need your AWS Access Key ID and Secret Access Key.
5. **AWS S3 Bucket**: Create an S3 bucket where videos will be temporarily stored.
6. **AWS DynamoDB Table**: Create a DynamoDB table (e.g., `YT_Video_ID_Table`) with `VideoID` as the primary key.

## Installation

You can install CloudVoy using `pip`. Ensure you have `pip` installed and updated.

```bash
pip install CloudVoy
```

## Configuration

CloudVoy uses environment variables to manage configurations securely. Follow the steps below to set up your environment.

### 1. Clone the Repository

If you haven't already, clone the repository:

```bash
git clone https://github.com/div-yam/CloudVoy.git
cd CloudVoy
```

### 2. Create a .env File

Create a `.env` file in the root directory of the project to store your configuration variables. This file should never be committed to version control for security reasons. Ensure it's added to `.gitignore`.

**.env**

```env
# YouTube Configuration
YOUTUBE_API_KEY=your_youtube_api_key
YOUTUBE_PLAYLIST_ID=your_playlist_id

# Instagram Configuration
INSTAGRAM_ACCOUNT_ID=your_instagram_account_id
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token

# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_S3_BUCKET_NAME=your_s3_bucket_name
AWS_S3_REGION=your_s3_region

# DynamoDB Configuration
DYNAMODB_TABLE_NAME=YT_Video_ID_Table

# Other Configuration
DOWNLOAD_PATH=downloaded_videos
```

Replace the placeholder values (`your_*`) with your actual credentials and configuration details.

### 3. Install Dependencies

Ensure all required dependencies are installed. If you installed via pip, this should be handled automatically. Otherwise, install them using `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Usage

CloudVoy provides two primary methods for uploading videos to Instagram:

### 1. Upload a Single Video Using a YouTube Link

This method allows you to upload a specific YouTube video to Instagram Reels by providing its URL.

**Example**

```python
from cloudvoy import upload_to_instagram_using_link

# Replace with your YouTube video URL
video_url = "https://www.youtube.com/watch?v=VIDEO_ID"

# Optional: Specify the video ID and title (caption)
# upload_to_instagram_using_link(video_url, video_id="VIDEO_ID", title="Your Caption")
upload_to_instagram_using_link(video_url)
```

**Parameters**
- `video_url` (str): The full URL of the YouTube video you wish to upload.
- `video_id` (str, optional): The unique identifier of the YouTube video. If not provided, it will be extracted from the URL.
- `title` (str, optional): The caption for the Instagram Reel. If not provided, the video title from YouTube will be used.

### 2. Upload All Today's Videos from Your Playlist

This method scans your specified YouTube playlist for any videos uploaded on the current day (in Indian Standard Time) and uploads them to Instagram Reels.

**Example**

```python
from cloudvoy import upload_instagram_today_videos

# Upload all videos from the playlist that were published today
upload_instagram_today_videos()
```

**Functionality**
- **Time Zone**: Determines the current day based on IST (Indian Standard Time).
- **Filtering**: Selects videos from the playlist that were published on the current day.
- **Upload Process**: For each qualifying video, it performs the upload workflow including downloading, uploading to S3, and publishing to Instagram.

## Examples

Here are some practical examples to help you get started with CloudVoy.

### Example 1: Uploading a Single Video

```python
from cloudvoy import upload_to_instagram_using_link

# Single YouTube video URL
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Upload the video to Instagram Reels
upload_to_instagram_using_link(video_url)
```

### Example 2: Uploading All Today's Videos

```python
from cloudvoy import upload_instagram_today_videos

# Upload all videos from the playlist that were published today
upload_instagram_today_videos()
```

### Example 3: Handling Errors and Logs

CloudVoy uses Python's logging module to provide detailed logs of the upload process. You can configure the logging level as needed.

```python
import logging
from cloudvoy import upload_to_instagram_using_link

# Configure logging to display DEBUG messages
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
upload_to_instagram_using_link(video_url)
```

## Testing

CloudVoy includes a suite of unit tests to ensure functionality remains intact during development and updates.

### Running Tests

Ensure you have all dependencies installed, then execute the following command from the root directory:

```bash
python -m unittest discover tests
```

### Test Coverage

The tests cover the primary functionalities of the library, including:

- Fetching videos from YouTube playlists.
- Downloading videos.
- Uploading to AWS S3.
- Interacting with Instagram Graph API.
- Managing upload status in DynamoDB.

**Note**: The tests use mocking to simulate external API interactions, ensuring they run quickly and without side effects.

## Contributing

Contributions are welcome! If you'd like to enhance CloudVoy, please follow these steps:

### Fork the Repository

Click the "Fork" button at the top right of the repository page to create your own fork.

### Create a New Branch

```bash
git checkout -b feature/YourFeatureName
```

### Make Your Changes

Implement your feature or bug fix. Ensure your code adheres to the existing coding standards.

### Commit Your Changes

```bash
git commit -m "Add your detailed description of the feature or fix"
```

### Push to Your Fork

```bash
git push origin feature
