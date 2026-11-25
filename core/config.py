from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    openai_api_key: str | None = None
    github_token: str | None = None
    database_path: Path = Path("data/codebase_whisperer.sqlite3")
    workspaces_dir: Path = Path("data/workspaces")
    chroma_dir: Path = Path("data/chroma")
    allowed_repos: str = ""
    answer_model: str = "gpt-4o-mini"
    rerank_model: str = "gpt-4o-mini"
    guide_model: str = "gpt-4o"
    openai_budget_usd: float = 30.0
    api_base_url: str = "http://localhost:8000"

    @property
    def allowed_repo_set(self) -> set[str]:
        return {item.strip().lower() for item in self.allowed_repos.split(",") if item.strip()}


@lru_cache
def get_settings() -> Settings:
    return Settings()
