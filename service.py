import uuid
import base64
from datetime import datetime
from storage import save_file, get_file_url, remove_file
from storage import save_metadata, get_metadata, delete_metadata, scan_metadata


def upload_image(data):
    user_id = data["user_id"]
    filename = data["filename"]
    image_base64 = data["image_base64"]
    tags = data.get("tags", [])

    image_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    file_bytes = base64.b64decode(image_base64)

    s3_key = f"{user_id}/{image_id}_{filename}"
    save_file(s3_key, file_bytes)

    metadata = {
        "user_id": user_id,
        "image_id": image_id,
        "filename": filename,
        "tags": tags,
        "created_at": created_at,
        "s3_key": s3_key
    }

    save_metadata(metadata)

    return metadata


def list_images(params):
    user_id = params["user_id"]
    tag_filter = params.get("tag")
    created_after = params.get("created_after")

    items = scan_metadata(user_id)

    if tag_filter:
        items = [i for i in items if tag_filter in i.get("tags", [])]

    if created_after:
        items = [i for i in items if i["created_at"] > created_after]

    return items


def get_image(user_id, image_id):
    item = get_metadata(user_id, image_id)
    if not item:
        raise Exception("Image not found")

    url = get_file_url(item["s3_key"])
    item["download_url"] = url
    return item


def delete_image(user_id, image_id):
    item = get_metadata(user_id, image_id)
    if not item:
        return {"deleted": False}

    remove_file(item["s3_key"])
    delete_metadata(user_id, image_id)

    return {"deleted": True}