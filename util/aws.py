import uuid

import boto3
import unicodedata
from botocore.client import Config
from botocore.exceptions import ClientError

from med.logger import Log
from med.settings import AWS_PUBLIC_BUCKET, AWS_REGION_NAME, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, ENV


def normalize_string(s: str):
    """Normalize a string to remove accents and other non-ascii characters"""

    if not s:
        return s
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def get_presigned_put_url(
        expiration=300,  # 300 seconds = 5 minutes,
        content_type=None,
):
    bucket = AWS_PUBLIC_BUCKET

    s3_config = {
        "service_name": "s3",
        "config": Config(
            signature_version="s3v4",
            s3={
                # "use_accelerate_endpoint": True,
                "addressing_style": "auto",
            },
        ),
        "region_name": AWS_REGION_NAME,
    }

    if ENV != "production":
        s3_config["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        s3_config["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY

    s3_client = boto3.client(**s3_config)

    params = {
        "Bucket": bucket,
        "Key": f"{uuid.uuid4()}",
    }
    final_url = f"https://{AWS_PUBLIC_BUCKET}.s3.{AWS_REGION_NAME}.amazonaws.com/{params['Key']}"

    params["StorageClass"] = "INTELLIGENT_TIERING"

    params["ContentType"] = content_type

    try:
        response = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params=params,
            ExpiresIn=expiration,
        )
    except ClientError as exc:
        Log.error(
            title="create_presigned_put (Code 1)",
            exc=exc,
        )
        return None

    return response, final_url
