import os
import boto3
import requests

DATA_URL = os.environ.get("DATA_URL")
FILE_NAME = os.environ.get("FILE_NAME")
BUCKET_NAME = os.environ.get("BUCKET_NAME")


def fetch_data(data_url):
    """Fetch file from {data_url}"""
    return requests.get(data_url).content


def lambda_handler(event, context):
    """AWS Lambda function."""
    s3 = boto3.resource('s3')

    print("[INFO] Request COVID-19 data...")
    data = fetch_data(DATA_URL)

    print(f"[INFO] Saving Data {FILE_NAME} to S3 Bucket {BUCKET_NAME}...")
    s3.Bucket(BUCKET_NAME).put_object(Key=FILE_NAME, Body=data)

    print(f"[INFO] Job done")


if __name__ == "__main__":
    lines = fetch_data(DATA_URL) \
        .decode() \
        .splitlines()

    for line in lines:
        print(line)
