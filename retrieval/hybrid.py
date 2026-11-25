"""Vector + FTS search with Reciprocal Rank Fusion (planned)."""

from core.schema import ScoredChunk


def retrieve(query: str, repos: list[str], source_types: list[str] | None = None, k: int = 8) -> list[ScoredChunk]:
    raise NotImplementedError("Hybrid retrieval and reranking are not implemented yet")
