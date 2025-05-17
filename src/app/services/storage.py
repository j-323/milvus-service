# src/app/services/storage.py

from minio import Minio
from app.core.config import settings
import json
import uuid
import time
from typing import Any

_client = Minio(
    endpoint=settings.s3.endpoint_url.replace("http://", ""),
    access_key=settings.s3.access_key,
    secret_key=settings.s3.secret_key,
    secure=False
)

_bucket = settings.s3.bucket
if not _client.bucket_exists(_bucket):
    _client.make_bucket(_bucket)

def upload_json(obj: dict[str, Any], prefix: str = "raw", retries: int = 3) -> str:
    """
    Загрузить JSON в MinIO с retry-бэкоффом.
    :param obj: любой сериализуемый в JSON объект, должен содержать 'track_id' или будет сгенерирован UUID
    :param prefix: 'raw' или 'enriched'
    :param retries: число попыток при ошибке
    :return: публичный URL загруженного файла
    """
    track_id = obj.get("track_id") or str(uuid.uuid4())
    key = f"{prefix}/{track_id}.json"
    blob = json.dumps(obj, ensure_ascii=False).encode("utf-8")

    for attempt in range(1, retries + 1):
        try:
            _client.put_object(
                bucket_name=_bucket,
                object_name=key,
                data=blob,
                length=len(blob),
                content_type="application/json"
            )
            return f"{settings.s3.endpoint_url}/{_bucket}/{key}"
        except Exception as e:
            if attempt < retries:
                # экспоненциальный бэкофф
                delay = 2 ** (attempt - 1)
                time.sleep(delay)
            else:
                raise RuntimeError(f"upload_json failed after {retries} attempts: {e}") from e