from fastapi import APIRouter
from app.models.schemas import SearchRequest, SearchResponse, SearchResult
from app.services.embeddings import embed_text
from app.services.milvus_client import search_vectors

router = APIRouter()

@router.post("", response_model=SearchResponse)
def search(req: SearchRequest):
    qvec = embed_text(req.query_text)
    raw_hits = search_vectors(qvec, top_k=req.top_k)

    results = []
    for hit in raw_hits:
        payload = hit.entity.get('payload', {})
        results.append(SearchResult(
            milvus_id=int(hit.id),
            score=hit.distance,
            metadata={k: v for k, v in payload.items() if k != "blob_enriched"},
            blob_url=payload.get("blob_enriched", "")
        ))
    return SearchResponse(results=results)