from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime

class Entity(BaseModel):
    text: str
    label: str
    start: int
    end: int

class Sentiment(BaseModel):
    polarity: float
    subjectivity: float

class Readability(BaseModel):
    flesch_reading_ease: float
    flesch_kincaid_grade: float

class Topic(BaseModel):
    topic_id: int
    terms: List[str]
    score: float

class SpotifyFeatures(BaseModel):
    tempo: float
    key: int
    mode: int
    time_signature: int
    loudness: float

class InternetMetadata(BaseModel):
    source: str
    fetched_at: datetime
    data: Dict[str, Any]

class EmbedRequest(BaseModel):
    track_id: int
    clean_text: str
    metadata: Dict[str, Any]

class EmbedResponse(BaseModel):
    status: str
    milvus_id: int

class SearchRequest(BaseModel):
    query_text: str
    top_k: int = 5

class SearchResult(BaseModel):
    milvus_id: int
    score: float
    metadata: Dict[str, Any]
    blob_url: str

class SearchResponse(BaseModel):
    results: List[SearchResult]