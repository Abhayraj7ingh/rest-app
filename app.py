import json
from service import upload_image, list_images, get_image, delete_image


def response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    method = event["httpMethod"]
    path = event["path"]

    try:
        if method == "POST" and path == "/images":
            body = json.loads(event["body"])
            return response(201, upload_image(body))

        if method == "GET" and path == "/images":
            params = event.get("queryStringParameters") or {}
            return response(200, list_images(params))

        if method == "GET" and path.startswith("/images/"):
            image_id = path.split("/")[-1]
            user_id = event["queryStringParameters"]["user_id"]
            return response(200, get_image(user_id, image_id))

        if method == "DELETE" and path.startswith("/images/"):
            image_id = path.split("/")[-1]
            user_id = event["queryStringParameters"]["user_id"]
            return response(200, delete_image(user_id, image_id))

        return response(404, {"message": "Not Found"})

    except Exception as e:
        return response(400, {"error": str(e)})