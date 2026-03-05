import os
import boto3

AWS_ENDPOINT = os.getenv("AWS_ENDPOINT_URL")  # for LocalStack
REGION = "us-east-1"

s3 = boto3.client("s3", endpoint_url=AWS_ENDPOINT, region_name=REGION)
dynamodb = boto3.resource("dynamodb", endpoint_url=AWS_ENDPOINT, region_name=REGION)

BUCKET = "images-bucket"
TABLE = "images-table"

table = dynamodb.Table(TABLE)


# ---------- S3 ----------

def save_file(key, data):
    s3.put_object(Bucket=BUCKET, Key=key, Body=data)


def get_file_url(key):
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": key},
        ExpiresIn=3600
    )


def remove_file(key):
    s3.delete_object(Bucket=BUCKET, Key=key)


# ---------- DynamoDB ----------

def save_metadata(item):
    table.put_item(Item=item)


def get_metadata(user_id, image_id):
    response = table.get_item(
        Key={"user_id": user_id, "image_id": image_id}
    )
    return response.get("Item")


def delete_metadata(user_id, image_id):
    table.delete_item(
        Key={"user_id": user_id, "image_id": image_id}
    )


def scan_metadata(user_id):
    response = table.scan(
        FilterExpression="user_id = :u",
        ExpressionAttributeValues={":u": user_id}
    )
    return response.get("Items", [])