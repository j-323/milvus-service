from fastapi import APIRouter, HTTPException
from app.models.schemas import EmbedRequest, EmbedResponse
from app.services.storage import upload_json
from app.services.embeddings import embed_text
from app.services.milvus_client import insert_vector
from app.services.text_analysis import analyze_text
from app.services.spotify_client import fetch_spotify_features
from app.services.perplexity_client import fetch_internet_metadata

router = APIRouter()

@router.post("", response_model=EmbedResponse)
def create_embed(req: EmbedRequest):
    raw_blob = {
        "track_id": req.track_id,
        "clean_text": req.clean_text,
        "metadata": req.metadata
    }
    raw_url = upload_json(raw_blob, prefix="raw")

    vec = embed_text(req.clean_text)

    analysis = analyze_text(req.clean_text)
    spotify_feats = fetch_spotify_features(req.metadata["artist"], req.metadata["title"])
    internet_meta = fetch_internet_metadata(f"{req.metadata['artist']} {req.metadata['title']}")

    enriched = {
        **req.metadata,
        "blob_raw": raw_url,
        "analysis": analysis,
        "spotify": spotify_feats,
        "internet_metadata": internet_meta
    }
    enriched_url = upload_json({"track_id": req.track_id, **enriched}, prefix="enriched")

    try:
        insert_vector(req.track_id, vec, {
            **enriched,
            "blob_enriched": enriched_url
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return EmbedResponse(status="ok", milvus_id=req.track_id)