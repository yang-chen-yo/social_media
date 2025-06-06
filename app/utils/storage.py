# app/utils/storage.py

import os, uuid
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "local")
UPLOAD_FOLDER   = os.getenv("UPLOAD_FOLDER", "static/images/")
IMAGE_BASE_URL  = os.getenv("IMAGE_BASE_URL", "/static/images/")

if STORAGE_BACKEND == "s3":
    import boto3
    from botocore.exceptions import ClientError

    AWS_REGION = os.getenv("AWS_REGION")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    S3_BUCKET = os.getenv("S3_BUCKET_NAME")

    # 建立 boto3 S3 client，直接使用環境變數
    s3_client = boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )


def save_image_file(image_file):
    """
    依 STORAGE_BACKEND 決定儲存邏輯：
    - local: 存到 local UPLOAD_FOLDER，回傳檔名
    - s3:    上傳到 S3 bucket posts/ 目錄，回傳檔名
    """
    # 把原始檔名轉乾淨
    original_name = secure_filename(image_file.filename)
    ext = os.path.splitext(original_name)[1]  # e.g. ".jpg"
    unique_name = f"{uuid.uuid4().hex}{ext}"

    if STORAGE_BACKEND == "local":
        # 本地端：把圖存到 UPLOAD_FOLDER
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        local_path = os.path.join(UPLOAD_FOLDER, unique_name)
        image_file.save(local_path)
        return unique_name

    elif STORAGE_BACKEND == "s3":
        key = f"posts/{unique_name}"
        try:
            # image_file.stream 是 werkzeug FileStorage 的 IO 物件
            s3_client.upload_fileobj(image_file.stream, S3_BUCKET, key)
            return unique_name
        except ClientError as e:
            # 上傳失敗時可以選擇拋例外或回傳 None
            raise e

    else:
        # fallback
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        local_path = os.path.join(UPLOAD_FOLDER, unique_name)
        image_file.save(local_path)
        return unique_name
