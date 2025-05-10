#!/usr/bin/env bash
python - <<EOF
from pymilvus import (
    connections, FieldSchema, CollectionSchema, DataType, Collection
)
import yaml

cfg = yaml.safe_load(open("configs/default.yaml"))
host = cfg["milvus"]["host"]
port = cfg["milvus"]["port"]

connections.connect("default", host=host, port=port)

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=1024),
    FieldSchema(name="payload", dtype=DataType.JSON)
]
schema = CollectionSchema(fields, description="Tracks embeddings")
if Collection.exists("tracks"):
    print("Collection 'tracks' already exists")
else:
    Collection(name="tracks", schema=schema)
    print("Created collection 'tracks'")
EOF