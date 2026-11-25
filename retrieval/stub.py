"""Fixture-backed retrieval placeholder for early agent/UI work."""

from core.schema import ScoredChunk


def retrieve(query: str, repos: list[str], source_types: list[str] | None = None, k: int = 8) -> list[ScoredChunk]:
    del query, repos, source_types, k
    return []
