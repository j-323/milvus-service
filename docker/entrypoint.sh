#!/usr/bin/env bash
set -e

# wait for Milvus
until nc -z ${MILVUS_HOST:-milvus} ${MILVUS_PORT:-19530}; do
  echo "Waiting for Milvus..."
  sleep 2
done

exec uvicorn src.app.main:app \
  --host ${SERVER_HOST:-0.0.0.0} \
  --port ${SERVER_PORT:-8000} \
  --log-config src/app/core/logger.py