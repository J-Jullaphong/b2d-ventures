import boto3
from botocore.exceptions import ClientError
from django.conf import settings


def get_file(key):
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_S3_REGION_NAME)
    try:
        url = s3.generate_presigned_url('get_object',
                                        Params={
                                            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                            'Key': key},
                                        ExpiresIn=3600)
        return url
    except ClientError as e:
        print(f"Error generating pre-signed URL: {e}")
        return None


def upload_file(file, key):
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_S3_REGION_NAME)
    try:
        s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, key)
        return True
    except ClientError as e:
        print(f"Error uploading file to S3: {e}")
        return False
