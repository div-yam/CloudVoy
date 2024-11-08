import logging
import boto3
from botocore.exceptions import ClientError
from .config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_S3_BUCKET_NAME,
    AWS_S3_REGION
)

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION
)

def upload_file_to_s3(file_path, s3_key):
    """Uploads a file to AWS S3."""
    try:
        s3_client.upload_file(
            file_path,
            AWS_S3_BUCKET_NAME,
            s3_key,
            ExtraArgs={'ACL': 'public-read', 'ContentType': 'video/mp4'}
        )
        logging.info(f"Uploaded {s3_key} to S3 bucket {AWS_S3_BUCKET_NAME}.")
        # Construct the public URL
        if AWS_S3_REGION == 'us-east-1':
            s3_url = f"https://{AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
        else:
            s3_url = f"https://{AWS_S3_BUCKET_NAME}.s3.{AWS_S3_REGION}.amazonaws.com/{s3_key}"
        return s3_url
    except ClientError as e:
        logging.error(f"Failed to upload {s3_key} to S3: {e}")
        return None

def delete_file_from_s3(s3_key):
    """Deletes a file from AWS S3."""
    try:
        s3_client.delete_object(Bucket=AWS_S3_BUCKET_NAME, Key=s3_key)
        logging.info(f"Deleted {s3_key} from S3 bucket {AWS_S3_BUCKET_NAME}.")
    except ClientError as e:
        logging.error(f"Failed to delete {s3_key} from S3: {e}")
