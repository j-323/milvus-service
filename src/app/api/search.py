# src/app/api/search.py

from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import conint
from app.models.schemas import SearchRequest, SearchResponse, SearchResult
from app.services.embeddings import embed_text
from app.services.milvus_client import search_vectors
from app.core.logger import logger

router = APIRouter()


@router.post("", response_model=SearchResponse)
async def search(req: SearchRequest):
    """
    1) Проверяем top_k (max 50)
    2) Генерируем вектор для запроса
    3) Делаем ANN-поиск в Milvus
    4) Формируем ответ
    """
    if not (1 <= req.top_k <= 50):
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 50")

    try:
        vec_tuple = await run_in_threadpool(embed_text, req.query_text)
        query_vec = list(vec_tuple)
        logger.debug(f"Search vector generated for query (len={len(query_vec)})")
    except Exception:
        logger.exception("Failed to generate embedding for search")
        raise HTTPException(status_code=502, detail="Embedding service failure")

    try:
        raw_hits = await run_in_threadpool(search_vectors, query_vec, req.top_k)
        logger.info(f"Found {len(raw_hits)} hits for query")
    except Exception:
        logger.exception("Milvus search failed")
        raise HTTPException(status_code=500, detail="Vector search failure")

    results = []
    for hit in raw_hits:
        payload = hit.entity.get("payload", {})
        results.append(SearchResult(
            milvus_id=int(hit.id),
            score=hit.distance,
            metadata={k: v for k, v in payload.items() if k != "blob_enriched"},
            blob_url=payload.get("blob_enriched", "")
        ))
    return SearchResponse(results=results)