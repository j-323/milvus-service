# src/app/services/embeddings.py

import openai
from functools import lru_cache
from transformers import AutoTokenizer, AutoModel
import torch
from app.core.config import settings

if settings.embedding.mode == "openai":
    openai.api_key = settings.embedding.openai.api_key
else:
    tokenizer = AutoTokenizer.from_pretrained(settings.embedding.local.model_name)
    model = AutoModel.from_pretrained(settings.embedding.local.model_name)

def embed_batch(texts: list[str]) -> list[list[float]]:
    """
    Сгенерировать эмбеддинги для списка строк.
    """
    if settings.embedding.mode == "openai":
        resp = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=texts
        )
        return [item["embedding"] for item in resp["data"]]
    else:
        inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return [emb.tolist() for emb in embeddings]

@lru_cache(maxsize=512)
def embed_text(text: str) -> tuple[float, ...]:
    """
    Сгенерировать эмбеддинг для одного текста.
    Результат кешируется (макс. 512 записей).
    """
    if settings.embedding.mode == "openai":
        resp = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        vec = resp["data"][0]["embedding"]
    else:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        vec = outputs.last_hidden_state.mean(dim=1)[0].tolist()

    # lru_cache не любит списки, упакуем в кортеж
    return tuple(vec)