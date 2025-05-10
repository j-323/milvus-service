from pydantic import BaseSettings, Field
import yaml

class PerplexitySettings(BaseSettings):
    api_url: str
    api_key: str

class AnalysisSettings(BaseSettings):
    spacy_model: str
    num_topics: int = Field(..., env="analysis.topic_modeling.num_topics")

class SpotifySettings(BaseSettings):
    client_id: str
    client_secret: str

class Settings(BaseSettings):
    milvus: dict
    s3: dict
    embedding: dict
    analysis: AnalysisSettings
    perplexity: PerplexitySettings
    spotify: SpotifySettings
    server: dict

    class Config:
        env_prefix = ""
        env_file = ".env"
        env_file_encoding = "utf-8"

cfg = yaml.safe_load(open("configs/default.yaml"))
settings = Settings(**cfg)