import copy
import io
from uuid import uuid4

import boto3
from PIL import Image
from django.core.files.base import ContentFile

from med.settings import AWS_PUBLIC_BUCKET, AWS_REGION_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, ENV


def upload_file(file, file_extension=None):

    s3_config = {
        "service_name": "s3",
        "region_name": AWS_REGION_NAME,
    }

    if ENV != "production":
        s3_config["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        s3_config["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY

    s3_client = boto3.client(**s3_config)

    if not file_extension:
        try:
            file_extension = file.name.split(".")[-1] or "png"
        except Exception:
            file_extension = "png"

    content_type = "image/png"
    if file_extension.lower() in ['jpeg', 'jpg']:
        content_type = "image/jpeg"

    file_name = f"{str(uuid4())}.{file_extension}"
    file_copy = copy.deepcopy(file)
    s3_client.upload_fileobj(file_copy, AWS_PUBLIC_BUCKET, str(file_name), ExtraArgs={'ContentType': content_type})
    url = f"https://{AWS_PUBLIC_BUCKET}.s3.{AWS_REGION_NAME}.amazonaws.com/{file_name}"
    return url


# def resize_image(file, size=(800, 800)):
#     """Resizes an image to the specified size."""
#     img = Image.open(file)
#     img.thumbnail(size)
#
#     # Create a BytesIO object
#     img_byte_arr = io.BytesIO()
#
#     # Convert PIL Image to Bytes
#     img.save(img_byte_arr, format='PNG')
#     img_byte_arr.seek(0)
#     return img_byte_arr

def get_reduced_size_content_file(file, resize_limit=128, file_format=None):
    img = Image.open(file)
    w = img.width
    h = img.height

    if w > h:
        h = h * resize_limit / w
        w = resize_limit
    else:
        w = w * resize_limit / h
        h = resize_limit

    resized_pil_img = img.resize(size=(int(w), int(h)), resample=Image.LANCZOS)

    if file_format and file_format.lower() in ['jpeg', 'jpg']:
        file_format = 'JPEG'
        resized_pil_img = resized_pil_img.convert('RGB')

    stream = io.BytesIO()
    resized_pil_img.save(stream, format=file_format or img.format or "PNG")
    content_file = ContentFile(stream.getvalue())

    # close streams
    resized_pil_img.close()

    return content_file
