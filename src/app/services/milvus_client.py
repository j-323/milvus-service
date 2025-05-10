from pymilvus import connections, Collection
from app.core.config import settings
from app.models.milvus_models import get_tracks_schema

connections.connect(
    alias="default",
    host=settings.milvus["host"],
    port=settings.milvus["port"]
)

collection_name = "tracks"
if not Collection.exists(collection_name):
    schema = get_tracks_schema()
    Collection(name=collection_name, schema=schema)

tracks_col = Collection(collection_name)

def insert_vector(id: int, vector: list[float], payload: dict) -> None:
    entities = [
        [id],
        [vector],
        [payload]
    ]
    tracks_col.insert(entities)
    tracks_col.flush()

def search_vectors(query_vec: list[float], top_k: int = 5):
    results = tracks_col.search(
        data=[query_vec],
        anns_field="vector",
        param={"metric_type": "L2", "params": {"nprobe": 10}},
        limit=top_k,
        expr=None
    )
    return results[0]