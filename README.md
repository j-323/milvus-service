# Service3-Embed

Микросервис для хранения текстовых промежуточных данных, расширенного анализа и эмбеддингов в Milvus.

## Запуск локально

1. Склонировать репозиторий  
2. Скопировать `configs/default.yaml` в `.env` или создать `.env` с нужными переменными  
3. `docker-compose up --build`  
4. `./scripts/init_milvus.sh`

## API

### POST /embed

```json
{
  "track_id": 123,
  "clean_text": "lyrics here …",
  "metadata": {"title":"Song","artist":"Artist"}
}