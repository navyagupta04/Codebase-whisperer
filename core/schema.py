from dataclasses import dataclass, field
from typing import Literal

from pydantic import BaseModel, Field

SourceType = Literal["code", "doc", "issue", "pr", "commit"]
ClaimType = Literal["verified", "inferred"]


class Chunk(BaseModel):
    chunk_id: str
    repo: str
    source_type: SourceType
    path: str
    symbol: str | None = None
    language: str | None = None
    start_line: int = Field(ge=1)
    end_line: int = Field(ge=1)
    commit_sha: str
    text: str
    content_hash: str
    meta: dict[str, object] = Field(default_factory=dict)


@dataclass
class ScoredChunk:
    chunk: Chunk
    score: float
    trace: dict[str, float | int | None] = field(default_factory=dict)


class Claim(BaseModel):
    text: str
    type: ClaimType
    chunk_ids: list[str] = Field(default_factory=list)


class AgentAnswer(BaseModel):
    claims: list[Claim] = Field(default_factory=list)
    not_found: bool = False
    missing_info: str | None = None


class RepositoryRegistration(BaseModel):
    url: str


class RepositoryRegistrationResult(BaseModel):
    canonical_url: str
    status: Literal["unsupported", "pending", "indexing", "ready", "failed"]
    decision: Literal["reuse", "ingest", "reject"]
    workspace_url: str | None = None
    indexed_sha: str | None = None
    message: str | None = None
