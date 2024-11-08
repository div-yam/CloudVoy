import unittest
from unittest.mock import patch
from cloudvoy import upload_to_instagram_using_link, upload_instagram_today_videos
from datetime import datetime

class TestCloudVoy(unittest.TestCase):

    @patch('cloudvoy.youtube.get_playlist_videos')
    @patch('cloudvoy.downloader.download_video')
    @patch('cloudvoy.s3_uploader.upload_file_to_s3')
    @patch('cloudvoy.instagram_uploader.upload_reel')
    @patch('cloudvoy.instagram_uploader.get_status_code')
    @patch('cloudvoy.instagram_uploader.publish_video')
    def test_upload_to_instagram_using_link(
        self, mock_publish_video, mock_get_status_code, mock_upload_reel,
        mock_upload_file_to_s3, mock_download_video, mock_get_playlist_videos
    ):
        # Setup mock responses
        mock_get_playlist_videos.return_value = [{
            'title': 'Test Video',
            'video_id': 'testid',
            'video_url': 'https://www.youtube.com/watch?v=testid',
            'published_at': '2023-10-10T00:00:00Z'
        }]
        mock_download_video.return_value = True
        mock_upload_file_to_s3.return_value = 'https://s3.amazonaws.com/bucket/testid.mp4'
        mock_upload_reel.return_value = {'id': 'ig_container_id'}
        mock_get_status_code.return_value = 'FINISHED'
        mock_publish_video.return_value = {'id': 'ig_media_id'}

        # Execute the method
        upload_to_instagram_using_link('https://www.youtube.com/watch?v=testid')

        # Assertions to ensure all steps were called
        mock_download_video.assert_called_once()
        mock_upload_file_to_s3.assert_called_once()
        mock_upload_reel.assert_called_once()
        mock_get_status_code.assert_called()
        mock_publish_video.assert_called_once()

    @patch('cloudvoy.youtube.get_playlist_videos')
    @patch('cloudvoy.upload_to_instagram_using_link')
    def test_upload_instagram_today_videos(self, mock_upload, mock_get_playlist_videos):
        # Setup mock responses
        mock_get_playlist_videos.return_value = [{
            'title': 'Today Video',
            'video_id': 'todayid',
            'video_url': 'https://www.youtube.com/watch?v=todayid',
            'published_at': datetime.utcnow().isoformat() + 'Z'
        }]

        # Execute the method
        upload_instagram_today_videos()

        # Assertions to ensure upload was called
        mock_upload.assert_called_once()

if __name__ == '__main__':
    unittest.main()
