# src/app/api/embed.py

from fastapi import APIRouter, HTTPException, BackgroundTasks, status
from fastapi.concurrency import run_in_threadpool
from app.models.schemas import EmbedRequest, EmbedResponse
from app.services.storage import upload_json
from app.services.embeddings import embed_text
from app.services.milvus_client import insert_vector
from app.core.logger import logger

router = APIRouter()


@router.post("", response_model=EmbedResponse, status_code=status.HTTP_201_CREATED)
async def create_embed(
    req: EmbedRequest,
    background_tasks: BackgroundTasks
):
    """
    1) Загружаем raw JSON в S3/MinIO
    2) Генерируем эмбеддинг (offloaded to threadpool)
    3) Сохраняем основную запись в Milvus
    4) Фоновая загрузка enriched JSON
    """
    raw_blob = {"track_id": req.track_id, "clean_text": req.clean_text, "metadata": req.metadata}
    try:
        raw_url = await run_in_threadpool(upload_json, raw_blob, "raw")
        logger.info(f"[{req.track_id}] Raw JSON uploaded: {raw_url}")
    except Exception as e:
        logger.exception(f"[{req.track_id}] Failed to upload raw JSON")
        raise HTTPException(status_code=500, detail="Cannot store raw data")

    try:
        vec_tuple = await run_in_threadpool(embed_text, req.clean_text)
        vec = list(vec_tuple)
        logger.debug(f"[{req.track_id}] Embedding generated (len={len(vec)})")
    except Exception as e:
        logger.exception(f"[{req.track_id}] Embedding generation failed")
        raise HTTPException(status_code=502, detail="Embedding service failure")

    enriched_payload = {**req.metadata, "blob_raw": raw_url}
    try:
        await run_in_threadpool(insert_vector, req.track_id, vec, enriched_payload)
        logger.info(f"[{req.track_id}] Vector inserted into Milvus")
    except Exception as e:
        logger.exception(f"[{req.track_id}] Milvus insert failed")
        raise HTTPException(status_code=500, detail="Vector storage failure")
    
    enriched_blob = {"track_id": req.track_id, **enriched_payload}
    background_tasks.add_task(upload_json, enriched_blob, "enriched")
    logger.info(f"[{req.track_id}] Scheduled enriched JSON upload")

    return EmbedResponse(status="ok", milvus_id=req.track_id)