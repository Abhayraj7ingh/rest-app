import base64
import pytest
from unittest.mock import patch

from service import upload_image, list_images, get_image, delete_image


# ---------------------------
# Upload Image
# ---------------------------
@patch("service.save_file")
@patch("service.save_metadata")
def test_upload_image(mock_save_metadata, mock_save_file):

    img = base64.b64encode(b"testdata").decode()

    data = {
        "user_id": "user1",
        "filename": "photo.png",
        "image_base64": img,
        "tags": ["food"]
    }

    result = upload_image(data)

    assert result["user_id"] == "user1"
    assert result["filename"] == "photo.png"
    assert "image_id" in result
    assert "created_at" in result

    mock_save_file.assert_called_once()
    mock_save_metadata.assert_called_once()


# ---------------------------
# List Images (with filters)
# ---------------------------
@patch("service.scan_metadata")
def test_list_images_with_tag_filter(mock_scan):

    mock_scan.return_value = [
        {"user_id": "u1", "tags": ["food"], "created_at": "2025"},
        {"user_id": "u1", "tags": ["travel"], "created_at": "2025"}
    ]

    params = {"user_id": "u1", "tag": "food"}

    result = list_images(params)

    assert len(result) == 1
    assert result[0]["tags"] == ["food"]


# ---------------------------
# Get Image Success
# ---------------------------
@patch("service.get_file_url")
@patch("service.get_metadata")
def test_get_image_success(mock_get_metadata, mock_get_url):

    mock_get_metadata.return_value = {
        "user_id": "u1",
        "image_id": "img1",
        "s3_key": "u1/img1_photo.png"
    }

    mock_get_url.return_value = "http://download-url"

    result = get_image("u1", "img1")

    assert result["download_url"] == "http://download-url"


# ---------------------------
# Get Image Not Found
# ---------------------------
@patch("service.get_metadata")
def test_get_image_not_found(mock_get_metadata):

    mock_get_metadata.return_value = None

    with pytest.raises(Exception):
        get_image("u1", "img1")


# ---------------------------
# Delete Image Success
# ---------------------------
@patch("service.remove_file")
@patch("service.delete_metadata")
@patch("service.get_metadata")
def test_delete_image_success(mock_get_metadata, mock_delete_metadata, mock_remove_file):

    mock_get_metadata.return_value = {
        "user_id": "u1",
        "image_id": "img1",
        "s3_key": "u1/img1_photo.png"
    }

    result = delete_image("u1", "img1")

    assert result["deleted"] is True

    mock_remove_file.assert_called_once()
    mock_delete_metadata.assert_called_once()


@patch("service.get_metadata")
def test_delete_image_not_found(mock_get_metadata):

    mock_get_metadata.return_value = None

    result = delete_image("u1", "img1")

    assert result["deleted"] is False