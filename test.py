import base64
from service import upload_image, list_images


def test_upload():
    img = base64.b64encode(b"hello").decode()

    data = {
        "user_id": "u1",
        "filename": "test.png",
        "image_base64": img,
        "tags": ["food"]
    }

    result = upload_image(data)

    assert result["user_id"] == "u1"
    assert "image_id" in result


def test_list():
    params = {"user_id": "u1"}
    result = list_images(params)
    assert isinstance(result, list)