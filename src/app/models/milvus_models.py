from pymilvus import FieldSchema, CollectionSchema, DataType

def get_tracks_schema(dim: int = 1024):
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name="payload", dtype=DataType.JSON)
    ]
    return CollectionSchema(fields, description="Tracks embeddings")