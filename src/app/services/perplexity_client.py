import requests
from datetime import datetime
from app.core.config import settings

def fetch_internet_metadata(query: str) -> dict:
    resp = requests.post(
        settings.perplexity.api_url,
        json={"query": query},
        headers={"Authorization": f"Bearer {settings.perplexity.api_key}"}
    )
    resp.raise_for_status()
    data = resp.json()
    return {
        "source": "perplexity",
        "fetched_at": datetime.utcnow().isoformat(),
        "data": data
    }