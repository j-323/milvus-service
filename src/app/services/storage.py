from minio import Minio
from app.core.config import settings
import json
import uuid

_client = Minio(
    endpoint=settings.s3.endpoint_url.replace("http://", ""),
    access_key=settings.s3.access_key,
    secret_key=settings.s3.secret_key,
    secure=False
)

_bucket = settings.s3.bucket
if not _client.bucket_exists(_bucket):
    _client.make_bucket(_bucket)

def upload_json(obj: dict, prefix: str = "raw") -> str:
    blob = json.dumps(obj).encode("utf-8")
    key = f"{prefix}/{obj.get('track_id', uuid.uuid4())}.json"
    _client.put_object(_bucket, key, data=blob, length=len(blob), content_type="application/json")
    return f"{settings.s3.endpoint_url}/{_bucket}/{key}"