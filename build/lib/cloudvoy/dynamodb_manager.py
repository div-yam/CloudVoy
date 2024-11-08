import logging
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import random
from .config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_S3_REGION,
    DYNAMODB_TABLE_NAME
)

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION
)

dynamodb_table = dynamodb.Table(DYNAMODB_TABLE_NAME)

def save_video_details(video_id, upload_status, instagram_publish_time, video_upload_date, title=None):
    """Saves or updates video details in DynamoDB."""
    try:
        item = {
            'VideoID': video_id,
            'upload_status': upload_status,
            'video_upload_date': video_upload_date
        }
        if title:
            item['title'] = title
        if instagram_publish_time:
            item['instagram_publish_time'] = instagram_publish_time
        dynamodb_table.put_item(
            Item=item,
            ConditionExpression="attribute_not_exists(VideoID) OR upload_status <> :success",
            ExpressionAttributeValues={
                ':success': 'success'
            }
        )
        logging.info(f"Saved/Updated video details in DynamoDB for video ID: {video_id}")
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            logging.info(f"Video ID {video_id} already has upload_status='success'. Skipping update.")
        else:
            logging.error(f"An error occurred while saving to DynamoDB: {e}")

def get_upload_status(video_id):
    """Retrieves the upload status of a video from DynamoDB."""
    try:
        response = dynamodb_table.get_item(
            Key={'VideoID': video_id},
            ProjectionExpression='upload_status'
        )
        return response.get('Item', {}).get('upload_status', 'not_uploaded')
    except ClientError as e:
        logging.error(f"An error occurred while fetching upload status from DynamoDB: {e}")
        return 'not_uploaded'

def get_random_video():
    """Fetches a random video with upload_status 'NOT_UPLOADED'."""
    try:
        response = dynamodb_table.scan(
            FilterExpression=Key('upload_status').eq('NOT_UPLOADED'),
            ProjectionExpression='VideoID, video_upload_date, title'
        )
        items = response.get('Items', [])
        if not items:
            logging.info("No videos found in DynamoDB with status 'NOT_UPLOADED'.")
            return None
        random_item = random.choice(items)
        return random_item
    except ClientError as e:
        logging.error(f"An error occurred while fetching random video from DynamoDB: {e}")
        return None
