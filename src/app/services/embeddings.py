import openai
from transformers import AutoTokenizer, AutoModel
import torch
from app.core.config import settings

if settings.embedding.mode == "openai":
    openai.api_key = settings.embedding.openai.api_key
else:
    tokenizer = AutoTokenizer.from_pretrained(settings.embedding.local.model_name)
    model = AutoModel.from_pretrained(settings.embedding.local.model_name)

def embed_text(text: str) -> list[float]:
    if settings.embedding.mode == "openai":
        resp = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        return resp["data"][0]["embedding"]
    else:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings[0].tolist()